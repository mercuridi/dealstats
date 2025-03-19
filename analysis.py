BUF_SIZE = 1024

def main():
    with open("125mil.txt", "r", encoding="utf8") as f:
        tmp_lines = f.readlines(BUF_SIZE)
        file_sum = 0
        i = 0
        while tmp_lines:
            #print(f"Block {i}")
            file_sum += sum(float(line) for line in tmp_lines)
            tmp_lines = f.readlines(BUF_SIZE)
            i += 1

    with open("125mil.txt", "rb", encoding="utf8") as f:
        num_lines = sum(1 for _ in f)

    print(num_lines)
    print(file_sum / num_lines)

if __name__ == "__main__":
    main()