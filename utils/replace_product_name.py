import fileinput
import os, fnmatch
import re

def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result
  
def apply_substitution(source_tree):
    files_to_replace = find('*.grd*', source_tree)
    files_to_replace.append(find('*.xtb', source_tree))
    
    for filename in files_to_replace:
      if not os.access(filename, os.W_OK):
        # If the patch cannot be written to, it cannot be opened for updating
        print(str(filename) + " cannot be opened for writing! Adding write permission...")
        path.chmod(filename.stat().st_mode | stat.S_IWUSR)
        
      with fileinput.FileInput(filename, inplace=True, backup='') as file:
          for line in file:
              print(re.sub(r'\bGoogle Chrome\b', 'Xempre Croma', line), end='')
              print(re.sub(r'\bChromium\b', 'Croma', line), end='')
              print(re.sub(r'\bChrome\b', 'Croma', line), end='')
              print(re.sub(r'\bChromiumOS\b', 'CromaOS', line), end='')
              print(re.sub(r'\bChromeOS\b', 'CromaOS', line), end='')
  
      
def main():
  apply_substitution('.')
  
if __name__ == '__main__':
    main()
