import os
import time
from datetime import datetime
import win32file
from struct import pack, unpack

# Default time range to search
DEFAULT_RANGE = 24 * 3600  # 1 day in seconds

# Global variables
time_range = 0

# Get epoch timestamp from date and time strings
def get_timestamp(date_str, time_str):
    date_format = '%Y-%m-%d'
    time_format = '%H:%M:%S'
    date = datetime.strptime(date_str, date_format)
    time = datetime.strptime(time_str, time_format)
    timestamp = date.timestamp() + time.hour * 3600 + time.minute * 60 + time.second
    return timestamp

# Check if a file can be recovered
def check_recoverable(filename, mtime):
    current_time = time.time()
    time_delta = current_time - mtime

    # File was modified within time range, so likely recoverable
    if time_delta <= time_range:
        print(f'{filename} was deleted within the time range. Recoverable!')
        return True

    # File was overwritten, so unlikely recoverable
    if os.path.exists(filename):
        print(f'{filename} was overwritten. Unrecoverable!')
        return False

    # File partially recoverable
    clusters = get_file_clusters(filename)
    if clusters is None:
        print(f'{filename} metadata not found. Unrecoverable!')
        return False
    used_clusters = set(get_used_clusters())
    recoverable_clusters = clusters - used_clusters
    if recoverable_clusters:
        print(f'{filename} has {len(recoverable_clusters)} recoverable clusters')
        return True

    # File found but unrecoverable
    print(f'{filename} found but unrecoverable!')
    return False

# Obtener lista de clústeres utilizados
def get_used_clusters():
    used_clusters = []
    drive_path = "C:"  # Reemplaza con la unidad que deseas analizar (por ejemplo, "C:", "D:", etc.)
    volume_path = fr"\\.\{drive_path}"
    volume_handle = win32file.CreateFile(volume_path, win32file.GENERIC_READ, win32file.FILE_SHARE_READ | win32file.FILE_SHARE_WRITE, None, win32file.OPEN_EXISTING, 0, None)
    _, bytes_per_sector, _ = win32file.GetDiskFreeSpace(drive_path)
    file_system_data = win32file.GetFileInformationByHandle(volume_handle)
    volume_serial_number = file_system_data[4]
    cluster_size = file_system_data[5]
    cluster_count = file_system_data[6] // cluster_size
    mft_start_cluster = file_system_data[7]
    mft_cluster_count = file_system_data[8]
    mft_data = win32file.DeviceIoControl(volume_handle, win32file.FSCTL_GET_NTFS_VOLUME_DATA, None, 2048)
    mft_bitmap = mft_data[64:64+mft_cluster_count//8]
    mft_bitmap_offset = mft_start_cluster * cluster_size // bytes_per_sector
    for i in range(mft_cluster_count):
        if mft_bitmap[i // 8] & (1 << (i % 8)):
            cluster = (mft_bitmap_offset + i) * bytes_per_sector // cluster_size
            used_clusters.extend(range(cluster, cluster + cluster_size))
    win32file.CloseHandle(volume_handle)
    return used_clusters

# Obtener lista de clústeres utilizados por un archivo dado
def get_file_clusters(filename):
    drive_path = "C:"  # Reemplaza con la unidad que deseas analizar (por ejemplo, "C:", "D:", etc.)
    volume_path = fr"\\.\{drive_path}"
    volume_handle = win32file.CreateFile(volume_path, win32file.GENERIC_READ, win32file.FILE_SHARE_READ | win32file.FILE_SHARE_WRITE, None, win32file.OPEN_EXISTING, 0, None)
    try:
        file_handle = win32file.CreateFile(filename, win32file.GENERIC_READ, win32file.FILE_SHARE_READ | win32file.FILE_SHARE_WRITE, None, win32file.OPEN_EXISTING, 0, None)
        file_data = win32file.GetFileInformationByHandle(file_handle)
        file_size = file_data[7]
        cluster_size = file_data[8]
        cluster_count = (file_size + cluster_size - 1) // cluster_size
        clusters = win32file.DeviceIoControl(volume_handle, win32file.FSCTL_GET_RETRIEVAL_POINTERS, pack("Q", file_data[8]), 1024)
        run_list = clusters[16:16+clusters[12]]
        file_clusters = []
        for i in range(len(run_list) // 16):
            start_vcn, start_lcn, cluster_count = unpack("QQQ", run_list[i*16:(i+1)*16])
            file_clusters.extend(range(start_lcn, start_lcn + cluster_count))
        return set(file_clusters)
    except Exception as e:
        print(f"Error al obtener los clústeres del archivo {filename}: {e}")
        return None
    finally:
        win32file.CloseHandle(volume_handle)


# Search disk and display recoverable files
def search_disk(start_path):
    recovered_files = []
    for dirpath, _, filenames in os.walk(start_path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            mtime = os.path.getmtime(filepath)  # Get last modified time of file
            if check_recoverable(filepath, mtime):
                print(filepath)  # Display recoverable file
                recovered_files.append(filepath)
    return recovered_files

# Get user time range input
def get_time_range_input():
    choice = input('Search by default time range (y/n)? ')
    if choice.lower() == 'y':
        return DEFAULT_RANGE
    date_str = input('Start date (YYYY-MM-DD): ')
    time_str = input('Start time (HH:MM:SS): ')
    start = get_timestamp(date_str, time_str)
    date_str = input('End date (YYYY-MM-DD): ')
    time_str = input('End time (HH:MM:SS): ')
    end = get_timestamp(date_str, time_str)
    return end - start

# Get user input for search path
def get_search_path():
    choice = input('Search the whole disk (y/n)? ')
    if choice.lower() == 'y':
        return None
    else:
        return input('Enter the directory path to search: ')

# Get user input for file selection
def select_files_to_recover(recovered_files):
    choice = input('Do you want to recover any files (y/n)? ')
    if choice.lower() == 'y':
        selected_files = []
        print('Select files to recover (enter file number or "done" to finish):')
        for i, filename in enumerate(recovered_files):
            print(f'{i+1}. {filename}')
        while True:
            file_choice = input()
            if file_choice.lower() == 'done':
                break
            try:
                file_index = int(file_choice) - 1
                if 0 <= file_index < len(recovered_files):
                    selected_files.append(recovered_files[file_index])
                    print(f'{recovered_files[file_index]} added to recovery list.')
                else:
                    print('Invalid file number.')
            except ValueError:
                print('Invalid input.')
        return selected_files
    else:
        return []

def main():
    global time_range
    time_range = get_time_range_input()
    search_path = get_search_path()
    if search_path is None:
        print('Searching the whole disk...')
        search_path = 'C:'
    else:
        print(f'Searching directory: {search_path}')
    recovered_files = search_disk(search_path)
    selected_files = select_files_to_recover(recovered_files)
    print('Files selected for recovery:')
    for filename in selected_files:
        print(filename)

# Start the program
if __name__ == '__main__':
    main()
