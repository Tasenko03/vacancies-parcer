seed = []


def get_urls(seed_l: list):
    for i in range(137):
        link = f"https://career.habr.com/vacancies?page={str(i)}&sort=date&type=all"
        seed_l.append(f"{link}")
    return seed_l


links = get_urls(seed)
print(links)
