from agent import run_agent

TESTS = [
    ("Who lives in Dallas?", ["Mika", "Dan", "Sol"]),
    ("Who lives in Austin?", ["Maria", "Niecy"]),
    ("Which people have no orders?", ["Dan", "Lucy", "Maria"]),
    ("Which people have a balance of 2000 or more?", ["Lisa", "Mika", "Maria", "Niecy"]),
    ("Who purchaced more than one product?", ["Mika", "Sol", "Sharky", "Lisa", "Junior", "Niecy"]),
    ("Who spent 500 or more?", ["Mika", "Sharky", "Junior"]),
    ("Which city has two people or more?", ["Dallas", "Houston", "Austin"]),
    ("What is a varible?", ["value", "notes1"]),
    ("What does it mean to chunk_by_size?", ["chunk", "pieces", "notes6"]),
    ("What does CRUD stand for?", ["create", "delete", "notes4"]),
    ("How much does Maria have in wallets, and what does JSON stand for?", ["10250", "javascript object notation", "notes3"]),
    ("What is Mika's age and city, and when dealing with API keys what should you never do?", ["36", "Dallas", "never", "directly", "notes3"]),
]
    
passed = 0
 
for question, must_contain in TESTS:
    answer, steps = run_agent(question)
    ok = all(word.lower() in answer.lower().replace(",", "") for word in must_contain)
    if ok:
        passed += 1
    print("PASS" if ok else "FAIL", "|", question)
    if not ok:
        print("   got:", answer[:200])
    
print(f"\nScore: {passed}/{len(TESTS)}")
