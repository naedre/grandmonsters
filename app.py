from flask import Flask, render_template_string
import requests
import time
import threading

app = Flask(__name__)

# =========================
# ALL USERS
# =========================
BOTS = [

    # your bots
    "rascal1","beastie1","calico1","osaurus","battlebornthe4th",
    "kowalabi","qioui","soulgar","rachl1","battlebornthe3rd",
    "nickl1bot","jembok","clementyne1","malpamat","battlebornthe2nd",
    "spyros1bot","lancelbot","goldinho1bot","ramanupo","battlebornthe1st",
    "hashcake1","reaper1bot","escarbo","genesis1bot",

    # team bots
    "RockingSuperstars",
    "mdbot",
    "pumpkinlattebob",
    "Balloon_L5",
    "Balloon_L4",
    "Balloon_L3",
    "Balloon_L2",
    "Balloon_L1",
    "uSunfish-l7",

    # humans
    "Artem_ZR",
    "Ren123456",
    "FeodorRo",
    "RuPsHa1235",
    "MatchaLatteBob",
    "XBLAAAA",
    "Zubarev_Nikolai",
    "hastingshastings",
]

# =========================
# HUMAN PLAYERS = GOLD
# =========================
HUMANS = set([
    "Artem_ZR",
    "Ren123456",
    "FeodorRo",
    "RuPsHa1235",
    "MatchaLatteBob",
    "XBLAAAA",
    "Zubarev_Nikolai",
    "hastingshastings",
])

# =========================
# YOUR BOTS = BRONZE
# =========================
MY_BOTS = set([
    "rascal1","beastie1","calico1","osaurus","battlebornthe4th",
    "kowalabi","qioui","soulgar","rachl1","battlebornthe3rd",
    "nickl1bot","jembok","clementyne1","malpamat","battlebornthe2nd",
    "spyros1bot","lancelbot","goldinho1bot","ramanupo","battlebornthe1st",
    "hashcake1","reaper1bot","escarbo","genesis1bot",
])

# =========================
# TEAM BOTS = SILVER
# =========================
TEAM_BOTS = set([
    "RockingSuperstars",
    "mdbot",
    "pumpkinlattebob",
    "Balloon_L5",
    "Balloon_L4",
    "Balloon_L3",
    "Balloon_L2",
    "Balloon_L1",
    "uSunfish-l7",
])

CACHE = {
    "data": [],
    "last_update": 0
}

# =========================
# RED -> PURPLE COLORS
# =========================
def color(value, vmin, vmax):

    if not isinstance(value, (int, float)):
        return "#666"

    if vmax == vmin:
        return "#999"

    t = (value - vmin) / (vmax - vmin)
    t = max(0, min(1, t))

    hue = t * 280

    return f"hsl({hue}, 85%, 60%)"


def safe(vals):
    return [v for v in vals if isinstance(v, (int, float))]


# =========================
# FETCH USER
# =========================
def resolve_user(username):

    try:

        r = requests.get(
            f"https://lichess.org/api/user/{username}",
            timeout=10
        )

        if r.status_code == 200:
            return r.json()

    except:
        pass

    return None


# =========================
# UPDATE LOOP
# =========================
def update_loop():

    global CACHE

    while True:

        try:

            ids = ",".join(BOTS)

            status_resp = requests.get(
                f"https://lichess.org/api/users/status?ids={ids}",
                timeout=10
            )

            statuses = {}

            if status_resp.status_code == 200:

                for s in status_resp.json():

                    statuses[s["id"].lower()] = s.get(
                        "online",
                        False
                    )

            results = []

            avgs = []
            bullets = []
            blitzes = []
            rapids = []
            classs = []

            c960 = []
            crazy = []
            koth = []
            three = []
            anti = []
            atomic = []
            horde = []
            racing = []

            for username in BOTS:

                try:

                    data = resolve_user(username)

                    if not data:
                        continue

                    perfs = data.get("perfs", {})
                    count = data.get("count", {})

                    def r(x):
                        return perfs.get(x, {}).get("rating")

                    bullet = r("bullet")
                    blitz = r("blitz")
                    rapid = r("rapid")
                    classical = r("classical")

                    chess960 = r("chess960")
                    crazyv = r("crazyhouse")
                    kothv = r("kingOfTheHill")
                    threev = r("threeCheck")
                    antiv = r("antichess")
                    atomicv = r("atomic")
                    hordev = r("horde")
                    racingv = r("racingKings")

                    ratings = [
                        x for x in [bullet, blitz, rapid]
                        if isinstance(x, int)
                    ]

                    weights = [1,2,1][:len(ratings)]

                    avg = (
                        sum(r*w for r,w in zip(ratings, weights))
                        / sum(weights)
                    ) if ratings else 0

                    avgs.append(avg)

                    bullets.append(bullet)
                    blitzes.append(blitz)
                    rapids.append(rapid)
                    classs.append(classical)

                    c960.append(chess960)
                    crazy.append(crazyv)
                    koth.append(kothv)
                    three.append(threev)
                    anti.append(antiv)
                    atomic.append(atomicv)
                    horde.append(hordev)
                    racing.append(racingv)

                    results.append({

                        "username": username,
                        "avg": round(avg),

                        "bullet": bullet,
                        "blitz": blitz,
                        "rapid": rapid,
                        "classical": classical,

                        "chess960": chess960,
                        "crazy": crazyv,
                        "koth": kothv,
                        "three": threev,
                        "anti": antiv,
                        "atomic": atomicv,
                        "horde": hordev,
                        "racing": racingv,

                        "games": count.get("all", 0),

                        "online": statuses.get(
                            username.lower(),
                            False
                        ),

                        "is_human": username in HUMANS,
                        "is_mine": username in MY_BOTS,
                        "is_team_bot": username in TEAM_BOTS,
                    })

                except:
                    continue

            ranges = {

                "avg": (
                    min(safe(avgs)),
                    max(safe(avgs))
                ),

                "bullet": (
                    min(safe(bullets)),
                    max(safe(bullets))
                ),

                "blitz": (
                    min(safe(blitzes)),
                    max(safe(blitzes))
                ),

                "rapid": (
                    min(safe(rapids)),
                    max(safe(rapids))
                ),

                "classical": (
                    min(safe(classs)),
                    max(safe(classs))
                ),

                "chess960": (
                    min(safe(c960)),
                    max(safe(c960))
                ),

                "crazy": (
                    min(safe(crazy)),
                    max(safe(crazy))
                ),

                "koth": (
                    min(safe(koth)),
                    max(safe(koth))
                ),

                "three": (
                    min(safe(three)),
                    max(safe(three))
                ),

                "anti": (
                    min(safe(anti)),
                    max(safe(anti))
                ),

                "atomic": (
                    min(safe(atomic)),
                    max(safe(atomic))
                ),

                "horde": (
                    min(safe(horde)),
                    max(safe(horde))
                ),

                "racing": (
                    min(safe(racing)),
                    max(safe(racing))
                ),
            }

            for r in results:
                r["ranges"] = ranges

            results.sort(
                key=lambda x: x["avg"],
                reverse=True
            )

            CACHE["data"] = results
            CACHE["last_update"] = time.time()

        except:
            pass

        time.sleep(180)


threading.Thread(
    target=update_loop,
    daemon=True
).start()

# =========================
# UI
# =========================
HTML = """

<!DOCTYPE html>
<html>

<head>

<title>Team Sagittarius Leaderboard</title>

<style>

body{
    background:#101010;
    color:white;
    font-family:Verdana, Tahoma, Arial, sans-serif;
    padding:14px;
    overflow-x:auto;
}

h1{
    margin-top:0;
    margin-bottom:12px;
    font-size:28px;
}

.topbar{
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap:12px;
    margin-bottom:12px;
    flex-wrap:wrap;
    background:#181818;
    border:1px solid #2d2d2d;
    border-radius:10px;
    padding:10px 14px;
}

.legend{
    display:flex;
    gap:18px;
    align-items:center;
    flex-wrap:wrap;
    font-size:13px;
    color:#ccc;
}

.legend span{
    font-weight:bold;
}

.refresh-btn{
    padding:7px 12px;
    background:#222;
    color:white;
    border:1px solid #444;
    border-radius:6px;
    cursor:pointer;
    font-size:13px;
}

.refresh-btn:hover{
    background:#2c2c2c;
}

.updated{
    color:#888;
    font-size:12px;
}

table{
    width:max-content;
    border-collapse:collapse;
    background:#181818;
    min-width:1300px;
}

th,td{
    padding:5px 7px;
    border-bottom:1px solid #2a2a2a;
    text-align:center;
    font-size:12px;
    white-space:nowrap;
}

th{
    background:#202020;
    position:sticky;
    top:0;
    z-index:2;
    font-size:11px;
    letter-spacing:0.5px;
}

tr:hover{
    background:rgba(255,255,255,0.04);
}

.bar{
    width:4px;
    padding:0;
}

.botname{
    text-align:left;
    font-weight:700;
    font-size:13px;
    min-width:180px;
}

.botname a{
    color:#f5f5f5;
    text-decoration:none;
}

.botname a:hover{
    color:white;
}

.dot{
    width:7px;
    height:7px;
    border-radius:50%;
    display:inline-block;
}

.online-dot{
    background:#4caf50;
}

.offline-dot{
    background:#666;
}

.goldstar{
    color:gold;
    font-size:13px;
}

.silverstar{
    color:silver;
    font-size:13px;
}

.bronzestar{
    color:#cd7f32;
    font-size:13px;
}

.rankcol{
    width:40px;
}

.smallcol{
    width:58px;
}

.gamescol{
    width:72px;
}

.statuscol{
    width:78px;
}

</style>

</head>

<body>

<h1>♟️ Sagittarius Chess Leaderboard</h1>

<div class="topbar">

    <div class="legend">

        <div>
            <span class="goldstar">★</span>
            Human Player
        </div>

        <div>
            <span class="silverstar">★</span>
            Team Bot
        </div>

        <div>
            <span class="bronzestar">★</span>
            Sagittarius Bot
        </div>

        <div class="updated">
            Last updated: {{ time }}
        </div>

    </div>

    <button
        onclick="location.reload()"
        class="refresh-btn"
    >
        🔄 Refresh
    </button>

</div>

<table>

<tr>

<th></th>

<th class="rankcol">#</th>

<th>Name</th>

<th class="smallcol">ELO</th>

<th class="smallcol">Bullet</th>
<th class="smallcol">Blitz</th>
<th class="smallcol">Rapid</th>
<th class="smallcol">Classical</th>

<th class="smallcol">960</th>
<th class="smallcol">CrazyH</th>
<th class="smallcol">KOTH</th>
<th class="smallcol">3Check</th>
<th class="smallcol">Anti</th>
<th class="smallcol">Atomic</th>
<th class="smallcol">Horde</th>
<th class="smallcol">RK</th>

<th class="gamescol">Games</th>
<th class="statuscol">Status</th>

</tr>

{% for bot in bots %}

<tr>

<td class="bar"
style="background:
{{ color(bot.avg, bot.ranges['avg'][0], bot.ranges['avg'][1]) }}">
</td>

<td>{{ loop.index }}</td>

<td class="botname">

<a href="https://lichess.org/@/{{ bot.username }}"
target="_blank">

{{ bot.username }}

{% if bot.is_human %}
<span class="goldstar">★</span>

{% elif bot.is_team_bot %}
<span class="silverstar">★</span>

{% elif bot.is_mine %}
<span class="bronzestar">★</span>
{% endif %}

</a>

</td>

<td style="color:
{{ color(bot.avg, bot.ranges['avg'][0], bot.ranges['avg'][1]) }}">
<b>{{ bot.avg }}</b>
</td>

<td style="color:
{{ color(bot.bullet, bot.ranges['bullet'][0], bot.ranges['bullet'][1]) }}">
{{ bot.bullet or "-" }}
</td>

<td style="color:
{{ color(bot.blitz, bot.ranges['blitz'][0], bot.ranges['blitz'][1]) }}">
{{ bot.blitz or "-" }}
</td>

<td style="color:
{{ color(bot.rapid, bot.ranges['rapid'][0], bot.ranges['rapid'][1]) }}">
{{ bot.rapid or "-" }}
</td>

<td style="color:
{{ color(bot.classical, bot.ranges['classical'][0], bot.ranges['classical'][1]) }}">
{{ bot.classical or "-" }}
</td>

<td style="color:
{{ color(bot.chess960, bot.ranges['chess960'][0], bot.ranges['chess960'][1]) }}">
{{ bot.chess960 or "-" }}
</td>

<td style="color:
{{ color(bot.crazy, bot.ranges['crazy'][0], bot.ranges['crazy'][1]) }}">
{{ bot.crazy or "-" }}
</td>

<td style="color:
{{ color(bot.koth, bot.ranges['koth'][0], bot.ranges['koth'][1]) }}">
{{ bot.koth or "-" }}
</td>

<td style="color:
{{ color(bot.three, bot.ranges['three'][0], bot.ranges['three'][1]) }}">
{{ bot.three or "-" }}
</td>

<td style="color:
{{ color(bot.anti, bot.ranges['anti'][0], bot.ranges['anti'][1]) }}">
{{ bot.anti or "-" }}
</td>

<td style="color:
{{ color(bot.atomic, bot.ranges['atomic'][0], bot.ranges['atomic'][1]) }}">
{{ bot.atomic or "-" }}
</td>

<td style="color:
{{ color(bot.horde, bot.ranges['horde'][0], bot.ranges['horde'][1]) }}">
{{ bot.horde or "-" }}
</td>

<td style="color:
{{ color(bot.racing, bot.ranges['racing'][0], bot.ranges['racing'][1]) }}">
{{ bot.racing or "-" }}
</td>

<td>{{ bot.games }}</td>

<td>

<span class="dot
{{ 'online-dot' if bot.online else 'offline-dot' }}">
</span>

{{ "ONLINE" if bot.online else "offline" }}

</td>

</tr>

{% endfor %}

</table>

</body>
</html>

"""

@app.route("/")
def index():

    readable_time = (
        time.strftime(
            "%H:%M:%S",
            time.localtime(CACHE["last_update"])
        )
        if CACHE["last_update"]
        else "never"
    )

    return render_template_string(
        HTML,
        bots=CACHE["data"],
        color=color,
        time=readable_time
    )

if __name__ == "__main__":
    app.run(debug=True, port=5000)