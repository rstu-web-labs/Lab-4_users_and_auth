import random
import string


class RandomLink:

    @staticmethod
    def random_link(length=8):
        return "".join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

    @staticmethod
    def array_random_links(count=100):
        array_links = [RandomLink.random_link() for _ in range(count)]
        return array_links


# if __name__ == "__main__":
#     print(RandomLink.array_random_links())
