import markovify


def main():
    print('Welcome to TrendyTwitter Bot!')
    with open("./lorem.txt") as file:
        string = file.read()
        print(string)

    text_model = markovify.Text(string)

    print(text_model.make_sentence())
    for i in range(3):
        print(text_model.make_short_sentence(140))


if __name__ == '__main__':
    main()
