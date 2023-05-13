import fileinput
import os, fnmatch
import re
from os import path
import stat

def find(pattern_list, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
          for pattern in pattern_list:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result

def find_not_binary(path):
    result = []
    
    for root, dirs, files in os.walk(path):
      for name in files:
        try:
          if 'src\\buildtools' not in str(root) and 'src\\third_party' not in str(root) and 'src\\tools' not in str(root):
            with open(str(os.path.join(root, name)), "r") as file:
              for l in file:
                pass
                
            if "chrome_exe" in str(name):
              os.rename(os.path.join(root, name), os.path.join(root, str(name).replace("chrome_exe", "croma_exe")))
              result.append(os.path.join(root, str(name).replace("chrome_exe", "croma_exe")))
            elif "chrome_dll" in str(name):
              os.rename(os.path.join(root, name), os.path.join(root, str(name).replace("chrome_dll", "croma_dll")))
              result.append(os.path.join(root, str(name).replace("chrome_dll", "croma_dll")))
            else:  
              result.append(os.path.join(root, name))
        except UnicodeDecodeError:
          pass # Found non-text data
    return result
  
def apply_substitution(source_tree):
    print("Start to find files")
    files_to_replace = find(['*.grd*', '*.xtb', 'BRANDING'], source_tree)
    print(len(files_to_replace), "total files (grd* + xtb + BRANDING)")

    print("Begin replacement")
    count = 1
    for filename in files_to_replace:
      if not os.access(filename, os.W_OK):
        # If the patch cannot be written to, it cannot be opened for updating
        print(str(filename) + " cannot be opened for writing! Adding write permission...")
        path.chmod(filename.stat().st_mode | stat.S_IWUSR)
      
      SOURCE_PREFIX = "build\\src\\"
      STR_START_POSITION = filename.find(SOURCE_PREFIX) + len(SOURCE_PREFIX)
      print(str('[' + str(count) + '/' + str(len(files_to_replace)) + '] ' + filename[STR_START_POSITION:]), flush = True, end = '\r')
      count += 1
      with fileinput.FileInput(filename, inplace=True, backup='', encoding='utf8') as file:
          for line in file:
              line = re.sub(r'\bGoogle Chrome\b', 'Xempre Croma', line)
              line = re.sub(r'\bGoogle Chromium\b', 'Xempre Croma', line)
              line = re.sub(r'\bChromium\b', 'Croma', line)
              line = re.sub(r'\bChrome\b', 'Croma', line)
              line = re.sub(r'\bChromiumOS\b', 'CromaOS', line)
              print(re.sub(r'\bChromeOS\b', 'CromaOS', line), end='')
          file.close()
    print("Finished replacement")

def apply_substitution_to_binaries_names(source_tree):
    print("Start to find files with no filter")
    files_to_replace = find_not_binary(source_tree)
    print(len(files_to_replace))

    print("Begin replacement")
    count = 1
    for filename in files_to_replace:
      try:
        if not os.access(filename, os.W_OK):
          # If the patch cannot be written to, it cannot be opened for updating
          print(str(filename) + " cannot be opened for writing! Adding write permission...")
          path.chmod(filename.stat().st_mode | stat.S_IWUSR)
        
        #print(str('Current file: ' + str(count) + ' - ' + filename).ljust(120, ' '), end='\r', flush=True)
        count += 1
        with fileinput.FileInput(filename, inplace=True, backup='', encoding='utf-8') as file:
            for line in file:
                line = re.sub(r'\bchrome.exe\b', 'croma.exe', line)
                line = re.sub(r'\bchrome.dll\b', 'croma.dll', line)
                line = re.sub(r'\bchrome_elf.dll\b', 'croma_elf.dll', line)
                line = re.sub(r'\bchrome_100_percent.pak\b', 'croma_100_percent.pak', line)
                line = re.sub(r'\bchrome_200_percent.pak\b', 'croma_200_percent.pak', line)
                line = re.sub(r'\bchrome_proxy.exe\b', 'croma_proxy.exe', line)
                line = re.sub(r'\bchrome_pwa_launcher.exe\b', 'croma_pwa_launcher.exe', line)
                line = re.sub(r'\bchrome_wer.dll\b', 'croma_wer.dll', line)
                print(line, end='')
                # line = re.sub(r'(?<![^\s"\\])chrome.exe(?![^\s"])', 'croma.exe', line)
                # line = re.sub(r'(?<![^\s"\\])chrome.dll(?![^\s"])', 'croma.dll', line)
                # line = re.sub(r'(?<![^\s"\\])chrome_elf.dll(?![^\s"])', 'croma_elf.dll', line)
                # line = re.sub(r'(?<![^\s"\\])chrome_100_percent.pak(?![^\s"])', 'croma_100_percent.pak', line)
                # line = re.sub(r'(?<![^\s"\\])chrome_200_percent.pak(?![^\s"])', 'croma_200_percent.pak', line)
                # line = re.sub(r'(?<![^\s"\\])chrome_proxy.exe(?![^\s"])', 'croma_proxy.exe', line)
                # line = re.sub(r'(?<![^\s"\\])chrome_pwa_launcher.exe(?![^\s"])', 'croma_pwa_launcher.exe', line)
                # print(re.sub(r'(?<![^\s"\\])chrome_wer.dll(?![^\s"])', 'croma_wer.dll', line), end='')
                # line = re.sub(r'chrome.exe', 'croma.exe', line)
                # line = re.sub(r'chrome.dll', 'croma.dll', line)
                # line = re.sub(r'chrome_elf.dll', 'croma_elf.dll', line)
                # line = re.sub(r'chrome_100_percent.pak', 'croma_100_percent.pak', line)
                # line = re.sub(r'chrome_200_percent.pak', 'croma_200_percent.pak', line)
                # line = re.sub(r'chrome_proxy.exe', 'croma_proxy.exe', line)
                # line = re.sub(r'chrome_pwa_launcher.exe', 'croma_pwa_launcher.exe', line)
                # print(re.sub(r'chrome_wer.dll', 'croma_wer.dll', line), end='')
            file.close()
      except:
        pass
    print("Finished replacement")
      
def main():
  apply_substitution('.')
  
if __name__ == '__main__':
    main()
