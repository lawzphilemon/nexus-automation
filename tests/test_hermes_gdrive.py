import importlib.util
import pathlib

root = pathlib.Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location('hermes_gdrive', root / 'scripts' / 'hermes-gdrive.py')
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)

assert g.doc_metadata('X') == {'name': 'X', 'mimeType': 'application/vnd.google-apps.document'}
assert g.doc_metadata('X', 'F')['parents'] == ['F']
assert g.format_comments([
    {'content': 'ganti H2', 'quotedFileContent': {'value': 'Apa itu CTR'}, 'replies': [{'content': 'ok'}, {'content': 'x', 'deleted': True}]},
    {'content': 'gone', 'deleted': True},
]) == [{'comment': 'ganti H2', 'on': 'Apa itu CTR', 'resolved': False, 'replies': ['ok']}]

# Every command the Hermes router can reach exists, and the router stays client-neutral.
skill = (root / '.hermes' / 'skills' / 'nexus' / 'SKILL.md').read_text(encoding='utf-8')
assert skill.startswith('---\nname: nexus\n')
assert 'hermes-gdrive.py' in skill and (root / 'commands' / 'queue.md').exists()
print('hermes gdrive test passed')
