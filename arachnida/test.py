r = requests.get(image_url, stream=True)
                    nombre_archivo = os.path.basename(image_url)
                    try:
                        with open(os.path.join(base_path, nombre_archivo), 'wb') as f:
                            r.raw.decode_content = True
                            shutil.copyfileobj(r.raw, f)
                    except Exception as e:
                        print(f"Error: {e}")