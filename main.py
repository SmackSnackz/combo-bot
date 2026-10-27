from agent import run_agent

def main(): 
    print("Ask about notes and the database. Type 'quit', or 'exit' to stop.")
    history = []
    while True:
        question = input("\nYou: ")
        if not question.strip():
            continue
        if question.strip().lower() in ("quit", "exit"):
            break
        answer, steps = run_agent(question, history)
        print(f"\nAgent: {answer}")
        print(f"\n[tools used: {[s['tool'] for s in steps]}]")

if __name__ == "__main__":
    main()