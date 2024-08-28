from chains.script_generation_chain import run_script_generation_chain

def main():
    user_input = input("Please enter your YouTube video idea: ")
    script = run_script_generation_chain(user_input)
    print("\nGenerated YouTube Script:")
    print(script)

if __name__ == "__main__":
    main()