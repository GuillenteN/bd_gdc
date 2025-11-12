# PR0203 Estructuras avanzadas de Redis

## Gestión de jugadores

### 1.  Función add_player(id, name, country, score)
```python
def add_player(player_id, name, country, score):
    player_key = f"player:{player_id}"
    r.hset(player_key, mapping={
        "name": name,
        "country": country,
        "games_played": 0,
        "score": score
    })
    r.zadd("leaderboard", {player_id: score})
```

### 2. Función update_score(id, points)
```python
def update_score(player_id, points):
    player_key = f"player:{player_id}"
    new_score = r.hincrbyfloat(player_key, "score", points)
    games_played = r.hincrby(player_key, "games_played", 1)
    r.zadd("leaderboard", {player_id: new_score})
```

### 3. Función player_info(id)
```python
def player_info(player_id):
    player_key = f"player:{player_id}"
    player_data = r.hgetall(player_key)
    return player_data
```

### 4. Función show_top_players(n)
```python
def show_top_players(n):
    leaderboard_key = "leaderboard"
    top_players = r.zrevrange(leaderboard_key, 0, n - 1, withscores=True)
    print(f"Top {n} jugadores del leaderboard:\n")
    print(top_players)
```

## Registro de actividad diaria (HyperLogLog)

### 1. Función register_login(player_id)
```python
from datetime import date
def register_login(player_id):
    fecha = date.today()
    key = f"unique:players:{fecha}"
    r.pfadd(key, player_id)
```

### 2. Función count_unique_logins(date)
```python

```

### 3. Función weekly_report(dates)
```python

```