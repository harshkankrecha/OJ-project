import os
import zipfile


def make_archive(zip_file_path, dir_to_compress, prefix):
    """
    :param zip_file_path: Creates a zip file at this path.
    :param dir_to_compress: Compresses all files in this given path.
    :param prefix: Adds this prefix to all the files when compressing them to archive.
    """
    with zipfile.ZipFile(zip_file_path, 'w') as zip_obj:
        for base_dir, extra_dirs, file_paths in os.walk(dir_to_compress):
            for file_path in file_paths:
                abs_path = os.path.join(base_dir, file_path)
                rel_path = os.path.relpath(abs_path, dir_to_compress)
                prefix_path = os.path.join("dragon_solutions", prefix, rel_path)
                zip_obj.write(abs_path, prefix_path)


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    zip_path = os.path.join(os.path.dirname(base_dir), 'dragon_solutions.zip')
    make_archive(zip_path, base_dir, prefix='dragons')
