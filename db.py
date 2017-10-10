from pydblite import Base

db = Base('QAData.pdl')

if db.exists():
    db.open()
else:
    db.create('question', 'answer', 'date', 'tags')
