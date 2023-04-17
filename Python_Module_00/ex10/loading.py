import time
import sys

def ft_progress(lst):
	length = len(lst)
	start_time = time.time()

	for i, item in enumerate(lst):
		percent_complete = (i + 1) * 100 / length
		elapsed_time = time.time() - start_time

		filled_slots = int(percent_complete / 5)
		empty_slots = 20 - filled_slots
 
		progress_bar = "[" + "=" * filled_slots + ">" + " " * empty_slots + "]"
		eta = (elapsed_time / (percent_complete / 100.00))

		sys.stdout.write("\r" + progress_bar + " " + str(percent_complete) + "% " + str(eta) + "s")
		sys.stdout.write("\rETA: {:.2f}s {} {:0.2f}% ({}/{}) | elapsed time {:.2f}s".format(eta, progress_bar,
									 percent_complete, i+1, length, elapsed_time))
		sys.stdout.flush()
		time.sleep(0.005)
		yield item

if __name__ == "__main__":
	lst = range(10)
	ret = 0
	for elem in ft_progress(lst):
		ret += elem
		time.sleep(0.5)
	print()
	print("...")
	print(ret)