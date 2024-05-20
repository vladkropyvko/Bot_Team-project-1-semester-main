import json 


def get_films(f_path:str = "app/data/films.json")->list:
    with open(f_path) as _:
        data = json.load(_)
        films = data.get("films")
        return films

def get_film(id:int=0, f_path:str = "app/data/films.json")->dict:
    return get_films(f_path)[id]


def save_film(film:dict = {}, f_path:str = "app/data/films.json")->bool:
    with open(f_path) as _:
        data = json.load(_)
        films = data.get("films")
        films.append(film)
    with open(f_path, "w") as _:
        json.dump(data, _, indent=4)
    return True

if __name__ == "__main__":
    print(get_films())