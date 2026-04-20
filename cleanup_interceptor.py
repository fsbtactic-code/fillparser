content = open('interceptor.py', 'rb').read().decode('utf-8-sig')
lines = content.splitlines(keepends=True)
clean = []
for l in lines:
    # Remove the orphaned garbage line from failed replacement
    if 'нагенерил' in l and 'split(' in l:
        continue
    clean.append(l)
open('interceptor.py', 'w', encoding='utf-8', newline='\n').writelines(clean)
print(f'Done: {len(lines)} -> {len(clean)} lines removed: {len(lines)-len(clean)}')
import ast
ast.parse(open('interceptor.py', 'r', encoding='utf-8').read())
print('OK syntax')
