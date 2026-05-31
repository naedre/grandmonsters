from flask import Flask, render_template_string
import requests, threading, time, os

app = Flask(__name__)

SAGITTARIUS_HUMANS = {"artem_zr", "Ren123456", "FeodorRo", "MatchaLatteBob", "Zubarev_Nikolai", "RuPsHa1235", "hastingshastings", "giabao204"}

GRAND_MONSTERS = {"battlebornthe1st", "battlebornthe2nd", "battlebornthe3rd", "battlebornthe4th", "rascal1", "beastie1", "calico1", "osaurus", "kowalabi", "qioui", "soulgar", "rachl1", "nickl1bot", "jembok", "clementyne1", "malpamat", "spyros1bot", "lancelbot", "goldinho1bot", "ramanupo", "hashcake1", "reaper1bot", "escarbo", "genesis1bot"}

TEAM_BOTS = {"RockingSuperstars", "MDBOT", "MDBOT2", "pumpkinlattebob", "eNErGyOFbEiNGbOT", "uSunfish-l0", "uSunfish-l1", "uSunfish-l7"}

RAW_ALL_BOTS = {"AaronsEngine", "abdcebot", "AconcaguaBot", "AdamantBot_V1", "admonitor", "AetherBot", "AggressiveStockfish", "ai-con", "ailedbot", "AKS-Mantissa", "Alexandrya", "AlPhAbEtACeta", "AlwaysPlayMystery", "AndrewYXZBot", "Anonymous_Bot2009", "anti-bot", "ArasanX", "ArkiPlaysChess", "AshNostromo", "athena-bot", "atwell-chess-bot", "AuraChessCNN", "Axiom_BOT", "baby_eubos", "Ballin-bot", "BattleBornThe1st", "BattleBornThe2nd", "BattleBornThe3rd", "BattleBornThe4th", "beastie1", "bernstein-2ply", "bernstein-4ply", "bestbotever", "bfiedler-bot", "Blobfish-Bot", "BorkaTower", "bot_adario", "Bot_Mittens", "Bot1221", "bot1500elo", "bot1e", "Bot1nokk", "Bot5551", "bot64jaques", "bot913", "BOTbotBOTbotBotrobot", "BOTMGMG", "BotWilsonator", "Botyuliirma", "BretemaBot", "Bullet_bot_0526", "byte-knight", "c0br4_bot", "C0kval", "caissa-x", "calico1", "canary_colinbot", "Capybara_ChessBOT", "Casanchess-NNUE", "CatNail", "Cerberus_bot", "cesium119", "CheckStudent", "chess_bot_faster", "chess-2-bot", "Chess3Bot", "ChessatronBot", "ChessBot2156", "chessbot2880", "Chessiverse_Ethan", "Chessiverse_Luc", "Chessiverse_Pawnza", "Chessiverse_Raak", "ChessNoobComp", "ChesssenseEngine", "chesstango_bot", "chestbot", "Cheszter", "chmod-bot", "Cimille", "cinder-bot", "Cizme", "Classic_BOT-v2", "ClassicLegendBot_v2", "clementyne1", "ClockworkEngine", "CloudBerk", "CloudNetBot", "coda_bot", "colinbot", "CosetteBot", "cppchessbot", "crabstick-engine", "croco_bot", "croco_little_bot", "CruelKen", "Ctrl_Alt_Destroy", "cybersoleil", "DaftNot", "dala-900", "DarkOnBot", "DavidsGuterBot", "debzero", "DeepBecky", "DefenchessOfficial", "Demolito_L1", "Demolito_L2", "Demolito_L3", "Demolito_L4", "Demolito_L5", "Demolito_L6", "DragonflyBOT", "DragonroseDev", "Drawcula_BOT", "Drunken-pipe-bomb", "duchessAI", "EdwardKillick", "Eichkatzerl", "escarbo", "eubos", "Euwe-chess-engine", "expositor", "FantasticFloyd", "FataliiBot", "fchess-bot", "FDG-Bot_1718", "felipe_bot_53", "Fischer_Bot", "follychess-com", "fornax-engine", "FoxChessBot", "FreddyyBot", "FunnyTheCat", "gage12_bot", "GameRoManBot", "GarboBot", "gekkammi-bot", "genesis1bot", "Genetic_Chess_Bot", "GlueWinner", "GNUPassant", "GoblinAjedrezAI", "Goldfish-Engine", "goldinho1bot", "Goopis", "grindle_x_bot1", "Groot123456", "GroshBoss", "GyatsoBot", "Haikuro-Bot", "HakoAI", "halcyonbot", "Hand_coded_ai_90565", "hashcake1", "HiusBot", "Humanoid_1800", "HumanTrainedBot", "Humuhumunukunukuapu", "Hyperopic", "HyZero", "icbmsaregoated2", "IgloBot", "IGotNoName", "ImranMelikovBot", "InanisBot", "io-bot", "ISARFish", "jangine", "JAXMAN_N", "jchess_engine", "JemBok", "Jibbby", "JomfishH", "joshsbot", "jpg-bot", "KarimBOT", "katzebot", "kflsddskflj", "khanhbell12345", "KiyEngine", "KnightFallBot", "kopyto_dev", "kowalabi", "Kwinibot", "Lancelbot", "larryz-alterego", "LeelaAnyOdds", "LeelaChessTest", "Licht94", "likeawizard-bot", "Lili-ai", "LimboBot", "LouisChess48-6K", "Lynx_BOT", "M8000_bot", "m8-bot", "Mac-Bot", "MAGIC11BOT", "malpamat", "MastacticaTeoriabot", "MateMakingMachine", "matmoi", "MCPeaSearch", "Meccedo", "mechasoleil", "MEGA-NOOB-BOT", "melsh_bot", "Meltd0wn", "MimirBot", "mjchess13", "mochi_bot", "Moment-That-Inspires", "Monastedrez", "morabandbot", "morphe157bot", "Mr_Sandbar", "Nakshatra3", "natto-bot", "nebubot", "NewChessEngine-ai", "newengine2022", "NexaStrat", "NICE_BOT", "nickl1bot", "NilatacBot", "Nimfish", "Novixxse", "nuttchess_bot", "Nyxite", "Obi-PawnKenoBOT", "odonata-bot", "OlympusCz", "OmbleCavalierPP", "OpeningsBot", "O-Rei-CX", "OSaurus", "Oxide9", "OxydanBot", "PARTNER3615DIAGO", "Pat9471", "PatriciaBot", "pawn_git", "pawnrobot", "PeachFruit", "pengyibot", "Perl-GigaChess", "pi0w", "piglet_engine", "Pix-Chess", "PlayMarius", "plisco-bot", "Plynder_3", "plynder_r6", "plynder_r8", "PositionalAI", "princhess_policy_bot", "Project_Nebulora", "prokopakop", "pruningBot", "puisne", "PumpkinLatteBob", "PureDefeat", "QiOui", "QuantumKnightV1", "QuantumKnightV2", "QueensGamBOT", "R0bspierre", "R4033", "rachl1", "RadianceEngine", "ramanupo", "rascal1", "RaspFish", "ratsu-bot", "Raven030", "RavenEngine", "RDI_Bot", "reaper1bot", "RecklessEngine", "RedHotBot", "RedSquirrelBot", "Reggz", "RenegadeEngine", "RobotJFischer", "RocketEngine", "RockingSuperstars", "Rodent-IV", "RookRusty", "RosaliaXadrez", "rudim-bot", "sargon-1ply", "sargon-2ply", "sargon-3ply", "sargon-4ply", "SaxtonEngine", "schnecken_bot", "SeitoGaKatsu", "SF_Bot1nok", "shaheris", "simbelmyne-bot", "simple-bot", "simpleEval", "simplexitor", "SleepMindEngine", "SleepyCPU", "slow-and-stupid", "slowmate_bot", "SmolStock", "SoloBot", "SomePythonBot", "soulgar", "spyros1bot", "sseh-c", "SteezyBot", "stickshark99", "StrawberryChess1", "StrawberryChessDev", "suniferia", "sxphia", "SybBot", "SykoraBot", "tbhOnBot", "Team_bot_08512", "TeamChelsie", "Terconari", "THANATOS_ENGINE_V7", "TheUnforgivingBot", "ThrorBjorn", "thunfisch-bot", "Tigrament", "tomahawkBOT", "tombot1234", "Toodfish", "TopasBot", "ToromBot", "TradeBot", "TroutBot", "turkjs", "TuroBot", "turochamp-1ply", "turochamp-2ply", "UltraBrick", "untrained4406", "Ursus_bot", "uSunfish-l0", "uSunfish-l1", "uSunfish-l7", "uxugin-bot", "uzenatch", "v7p3r_bot", "Valhalla-Bot", "vanibot", "Variant-bot", "varient-chess-bot1", "VietnameseCoffee", "Viet-Test", "ViolentStockfish", "virus_exe-bot", "Vividmind", "vixen_is_very_cool", "Void_Bot", "waychess-bot", "Weiawaga", "whychess-bot", "WildorderBot", "Windmolen_bot", "Wojtmic-Bot", "WoodStyleEngine", "Worst-ai", "WunderBot", "Xadreco", "Yellow_Anxiety7", "YoBot_v2", "YuliGPrO5", "Zagreus_Engine", "zeno-bot", "zero3-noW", "ZlomenyMesic"}

monsters_low, teambots_low = {m.lower() for m in GRAND_MONSTERS}, {t.lower() for t in TEAM_BOTS}
ALL_BOTS = {b for b in RAW_ALL_BOTS if b.lower() not in monsters_low and b.lower() not in teambots_low}.union(GRAND_MONSTERS, TEAM_BOTS)
USERS = sorted(list(SAGITTARIUS_HUMANS.union(ALL_BOTS)), key=str.casefold)
sagi_low = {h.lower() for h in SAGITTARIUS_HUMANS}

CACHE = {"data": [], "updated": "Never", "loading": True, "progress": "Starting initial ingestion..."}
FIELDS = [("avg", "ELO"), ("bullet", "Bullet"), ("blitz", "Blitz"), ("rapid", "Rapid"), ("classical", "Classical"), ("chess960", "960"), ("crazy", "Crazy"), ("koth", "KOTH"), ("three", "3C"), ("anti", "Anti"), ("atomic", "Atomic"), ("horde", "Horde"), ("racing", "RK"), ("puzzle", "Puzzle")]

session = requests.Session()
session.headers.update({"User-Agent": "SagittariusLeaderboard/2.0"})

def update_loop():
    global CACHE
    while True:
        try:
            CACHE["loading"] = True; statuses = {}
            for i in range(0, len(USERS), 25):
                try:
                    res = session.get(f"https://lichess.org/api/users/status?ids={','.join(USERS[i:i+25])}", timeout=10)
                    if res.status_code == 200:
                        for n in res.json(): statuses[n["id"].lower()] = n.get("online", False)
                except Exception as e: print(f"Status error: {e}")
                time.sleep(0.3)

            results, all_values = [], {k: [] for k, _ in FIELDS + [("games", "")]}

            for idx, username in enumerate(USERS, 1):
                CACHE["progress"] = f"Pacing safe profile mapping: {idx}/{len(USERS)} processed..."
                try:
                    res = session.get(f"https://lichess.org/api/user/{username}", timeout=10)
                    if res.status_code == 429: time.sleep(4); res = session.get(f"https://lichess.org/api/user/{username}", timeout=10)
                    if res.status_code != 200: continue
                    
                    data = res.json()
                    if data.get("tosViolation") or data.get("disabled") or data.get("closed"): continue
                    
                    u_low = username.lower()
                    is_sagi, is_grand, is_team, is_all = u_low in sagi_low, u_low in monsters_low, u_low in teambots_low, u_low in ALL_BOTS
                    
                    # Human filter stays strict, bots bypass games limit to capture all ~380 items
                    if is_sagi and data.get("count", {}).get("all", 0) < 120: continue

                    perfs, total_games = data.get("perfs", {}), data["count"]["all"]
                    rating = lambda name: perfs.get(name, {}).get("rating")
                    
                    r_list = [x for x in [rating("bullet"), rating("blitz"), rating("rapid")] if isinstance(x, (int, float))]
                    avg = round(sum(r_list) / len(r_list)) if r_list else None
                    has_var = any(isinstance(perfs.get(k, {}).get("rating"), (int, float)) for k in ["crazyhouse", "kingOfTheHill", "threeCheck", "antichess", "atomic", "horde", "racingKings"])

                    vals = {"avg": avg, "bullet": rating("bullet"), "blitz": rating("blitz"), "rapid": rating("rapid"), "classical": rating("classical"), "chess960": rating("chess960"), "crazy": rating("crazyhouse"), "koth": rating("kingOfTheHill"), "three": rating("threeCheck"), "anti": rating("antichess"), "atomic": rating("atomic"), "horde": rating("horde"), "racing": rating("racingKings"), "puzzle": rating("puzzle"), "games": total_games}
                    for k in all_values: all_values[k].append(vals[k])
                    
                    results.append({
                        "username": username, **vals, "online": statuses.get(u_low, False),
                        "is_sagittarius_human": is_sagi, "is_grandmonster": is_grand, "is_team_bot": is_team, "is_external_bot": is_all,
                        "is_rocking_superstar": not (is_sagi or is_grand or is_team or is_all), "is_variant_bot": (is_grand or is_team or is_all) and has_var
                    })
                except Exception as e: print(f"Error checking {username}: {e}")
                time.sleep(0.432) # Cut processing loop speed in half

            ranges = {k: (min(nums), max(nums)) if (nums := [v for v in values if isinstance(v, (int, float))]) else (0, 1) for k, values in all_values.items()}
            for row in results: row["ranges"] = ranges
            results.sort(key=lambda x: -(x["avg"] or 0))

            CACHE.update({"data": results, "updated": time.strftime("%Y-%m-%d %H:%M:%S"), "progress": f"Displaying records for {len(results)} users tracked.", "loading": False})
        except Exception as e: print(f"Global worker error: {e}"); time.sleep(10)
        time.sleep(1800)

if not hasattr(app, '_updater_started'):
    threading.Thread(target=update_loop, daemon=True).start()
    app._updater_started = True

HTML = """<!DOCTYPE html><html><head><title>The GrandMonsters Leaderboard</title><style>
*{box-sizing:border-box}body{margin:0;padding:20px;background:#0b0b12 radial-gradient(white,rgba(255,255,255,.15) 2px,transparent 40px) fixed;background-image:radial-gradient(white,rgba(255,255,255,.15) 2px,transparent 40px),radial-gradient(white,rgba(255,255,255,.1) 1px,transparent 30px),url('https://images.unsplash.com/photo-1506318137071-a8e063b4bec0?q=80&w=2000');background-size:550px 550px,350px 350px,cover;background-position:0 0,40px 60px,center;color:#e0e0ed;font-family:Verdana,sans-serif}
.container{display:table;float:left;margin:0;clear:both;background:rgba(14,14,26,.72);backdrop-filter:blur(14px);border-radius:14px;padding:18px;border:1px solid rgba(255,255,255,.06);box-shadow:0 20px 50px rgba(0,0,0,.6),0 0 40px rgba(100,70,180,.12)}
.main-title{margin-top:0;font-size:15px;color:#fff}.topbar{display:flex;justify-content:space-between;align-items:center;gap:20px;margin-bottom:16px;padding:10px 12px;border-radius:10px;background:rgba(30,30,50,.45);border:1px solid rgba(255,255,255,.05)}
.legend{display:flex;gap:8px}.legend-item{background:rgba(255,255,255,.05);padding:6px 10px;border-radius:6px;font-size:11px;white-space:nowrap;border:1px solid rgba(255,255,255,.08);color:#e0e0ed;cursor:pointer;transition:all .2s ease}
.legend-item:hover{background:rgba(255,255,255,.15);border-color:rgba(255,255,255,.25);transform:translateY(-1px)}
.legend-item.active-regular{background:rgba(120,80,255,.25);border-color:rgba(120,80,255,.6);box-shadow:0 0 10px rgba(120,80,255,.3);font-weight:700}
.legend-item.active-variant{background:rgba(6,182,212,.25);border-color:rgba(6,182,212,.6);box-shadow:0 0 10px rgba(6,182,212,.3);font-weight:700}
.legend-item.active-online{background:rgba(57,255,20,.25);border-color:rgba(57,255,20,.8);box-shadow:0 0 12px rgba(57,255,20,.4);font-weight:700;color:#adff2f}
.legend-item.active-variant-online{background:rgba(0,255,255,.25);border-color:rgba(0,255,255,.8);box-shadow:0 0 12px rgba(0,255,255,.4);font-weight:700;color:#00ffff}
.formula{font-size:11px;color:#d0d0ff;white-space:nowrap;padding:6px 12px;border-radius:8px;border:1px solid transparent;transition:all .3s cubic-bezier(.4,0,.2,1)}
.formula.highlight-regular{border-color:rgba(120,80,255,.7);background:rgba(120,80,255,.12);box-shadow:inset 0 0 8px rgba(120,80,255,.2),0 0 15px rgba(120,80,255,.4)}
.formula.highlight-variant{border-color:rgba(6,182,212,.7);background:rgba(6,182,212,.12);box-shadow:inset 0 0 8px rgba(6,182,212,.2),0 0 15px rgba(6,182,212,.4)}
.formula.highlight-online{border-color:rgba(57,255,20,.8);background:rgba(57,255,20,.1);box-shadow:inset 0 0 8px rgba(57,255,20,.2),0 0 18px rgba(57,255,20,.5);color:#adff2f;text-shadow:0 0 6px rgba(57,255,20,0.6)}
.formula.highlight-variant-online{border-color:rgba(0,255,255,.8);background:rgba(0,255,255,.1);box-shadow:inset 0 0 8px rgba(0,255,255,.2),0 0 18px rgba(0,255,255,.5);color:#00ffff;text-shadow:0 0 6px rgba(0,255,255,0.6)}
.refresh-area{display:flex;align-items:center;gap:10px;white-space:nowrap}.refresh-btn{background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.12);color:#fff;padding:5px 10px;border-radius:6px;cursor:pointer}
.refresh-btn:hover{background:rgba(255,255,255,.18)}.date{color:#8888aa;font-size:11px}table{width:auto;table-layout:auto;border-collapse:collapse;margin-bottom:15px}
th{background:rgba(35,35,60,.96);padding:8px 10px;font-size:11px;color:#b0b0ff;white-space:nowrap;cursor:pointer;user-select:none;position:relative}th:hover{background:rgba(45,45,80,.96);color:#fff}
td{padding:6px 10px;text-align:center;border-bottom:1px solid rgba(255,255,255,.04);font-size:11px;white-space:nowrap}td.name{text-align:left;font-weight:700;color:#fff}tr:hover{background:rgba(120,80,255,.12);cursor:pointer}
.online{color:#4caf50;font-weight:700}.offline{color:#666}.star-gold{color:gold}.star-silver{color:#ccd1d9}.star-bronze{color:#cd7f32}.star-white{color:#fff}
.loading-box{margin-top:20px;padding:12px;border-radius:10px;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.08)}
.loading{color:#ffd166;font-weight:700;font-size:11px;animation:blink 1s linear infinite}.done{color:#4caf50;font-weight:700;font-size:11px}
.progress{margin-top:5px;color:#ccccff;font-size:11px}@keyframes blink{0%,100%{opacity:1}50%{opacity:.3}}
</style></head><body><div class="container"><h1 class="main-title">🌌 The GrandMonsters Leaderboard</h1><div class="topbar"><div class="legend">
<button class="legend-item" data-category="sagi-human" onclick="handleCycleClick(this)"><span class="star-gold">★</span> Humans</button>
<button class="legend-item" data-category="monster" onclick="handleCycleClick(this)"><span id="monster-star" class="star-silver">★</span> GrandMonster Bots</button>
<button class="legend-item" data-category="team-bot" onclick="handleCycleClick(this)"><span class="star-bronze">★</span> Team Bots</button>
<button class="legend-item" data-category="external-bot" onclick="handleCycleClick(this)"><span id="external-star" class="star-white">★</span> All Bots</button></div>
<div class="formula" id="formula-txt"><b>ELO = (Bullet + Blitz + Rapid) ÷ 3</b></div><div class="refresh-area"><button class="refresh-btn" onclick="location.reload()">Refresh</button><span class="date">{{ updated }}</span></div></div>
<table id="leaderboard-table"><thead><tr><th onclick="sortTable(0)">#</th><th style="text-align:left;padding-left:10px;" onclick="sortTable(1)">Name</th>
{% for field, title in fields %}<th onclick="sortTable({{ loop.index + 1 }})" {% if field == 'avg' %}id="elo-th"{% endif %}>{{ title }}</th>{% endfor %}<th onclick="sortTable({{ fields|length + 2 }})">Games</th><th onclick="sortTable({{ fields|length + 3 }})">Status</th></tr></thead><tbody>
{% for bot in bots %}<tr data-sagihuman="{{ 'true' if bot.is_sagittarius_human else 'false' }}" data-rockinghuman="{{ 'true' if bot.is_rocking_superstar else 'false' }}" data-teambot="{{ 'true' if bot.is_team_bot else 'false' }}" data-monster="{{ 'true' if bot.is_grandmonster else 'false' }}" data-externalbot="{{ 'true' if bot.is_external_bot else 'false' }}" data-variantbot="{{ 'true' if bot.is_variant_bot else 'false' }}" data-bullet="{{ bot.bullet if bot.bullet != None else '' }}" data-blitz="{{ bot.blitz if bot.blitz != None else '' }}" data-rapid="{{ bot.rapid if bot.rapid != None else '' }}" data-classical="{{ bot.classical if bot.classical != None else '' }}" data-chess960="{{ bot.chess960 if bot.chess960 != None else '' }}" data-crazy="{{ bot.crazy if bot.crazy != None else '' }}" data-koth="{{ bot.koth if bot.koth != None else '' }}" data-three="{{ bot.three if bot.three != None else '' }}" data-anti="{{ bot.anti if bot.anti != None else '' }}" data-atomic="{{ bot.atomic if bot.atomic != None else '' }}" data-horde="{{ bot.horde if bot.horde != None else '' }}" data-racing="{{ bot.racing if bot.racing != None else '' }}" data-puzzle="{{ bot.puzzle if bot.puzzle != None else '' }}" data-games="{{ bot.games }}" data-online="{{ 'true' if bot.online else 'false' }}" data-defaultelo="{{ bot.avg if bot.avg != None else '-' }}" onclick="window.open('https://lichess.org/@/{{ bot.username }}','_blank')">
<td class="row-rank">{{ loop.index }}</td><td class="name">{{ bot.username }} <span class="badge-star">
{% if bot.is_sagittarius_human %}<span class="star-gold">★</span>{% elif bot.is_grandmonster %}<span class="star-silver">★</span>{% elif bot.is_team_bot %}<span class="star-bronze">★</span>{% elif bot.is_external_bot %}<span class="star-white">★</span>{% endif %}</span></td>
{% for field, title in fields %}<td {% if field == 'avg' %}class="elo-cell"{% endif %} style="font-weight:bold;">{{ bot[field] if bot[field] != None else "-" }}</td>{% endfor %}
<td class="games-cell" style="font-weight:bold;">{{ bot.games }}</td><td>{% if bot.online %}<span class="online">● ON</span>{% else %}<span class="offline">● off</span>{% endif %}</td></tr>{% endfor %}
</tbody></table><div class="loading-box">{% if loading %}<div class="loading">⏳ Reticulating splines...</div>{% else %}<div class="done">✅ Leaderboard fully updated</div>{% endif %}<div class="progress">{{ progress }}</div></div></div>
<script>
let sortDirections = {}, lastSortedColumn = 2;
function sortTable(columnIndex) {
    const table = document.getElementById("leaderboard-table"), tbody = table.getElementsByTagName("tbody")[0], rows = Array.from(tbody.getElementsByTagName("tr"));
    sortDirections[columnIndex] = !sortDirections[columnIndex];
    const ascending = sortDirections[columnIndex]; lastSortedColumn = columnIndex;
    rows.sort((rowA, rowB) => {
        let cellA = rowA.getElementsByTagName("td")[columnIndex].textContent.trim(), cellB = rowB.getElementsByTagName("td")[columnIndex].textContent.trim();
        let numA = (cellA === "-") ? 0 : parseFloat(cellA.replace(/[^\d.-]/g, '')), numB = (cellB === "-") ? 0 : parseFloat(cellB.replace(/[^\d.-]/g, ''));
        if (!isNaN(numA) && !isNaN(numB)) {
            if (!ascending) return (numA === 0 && numB !== 0) ? 1 : (numB === 0 && numA !== 0) ? -1 : numB - numA;
            return (numA === 0 && numB !== 0) ? 1 : (numB === 0 && numA !== 0) ? -1 : numA - numB;
        }
        return ascending ? cellA.localeCompare(cellB) : cellB.localeCompare(cellA);
    });
    rows.forEach(row => tbody.appendChild(row)); updateColorsAndRanks();
}
function updateColorsAndRanks() {
    const table = document.getElementById("leaderboard-table"), rows = Array.from(table.getElementsByTagName("tbody")[0].getElementsByTagName("tr")), visibleRows = rows.filter(row => row.style.display !== "none");
    let distinctVals = [];
    visibleRows.forEach((row, index) => {
        row.querySelector(".row-rank").innerText = index + 1;
        let cellVal = row.getElementsByTagName("td")[lastSortedColumn].textContent.trim();
        if (cellVal !== "-" && lastSortedColumn !== 1 && lastSortedColumn !== 16) {
            let num = parseFloat(cellVal.replace(/[^\d.-]/g, ''));
            if (!isNaN(num) && !distinctVals.includes(num)) distinctVals.push(num);
        }
    });
    distinctVals.sort((a, b) => a - b);
    
    let totalCount = distinctVals.length;

    visibleRows.forEach(row => {
        let cellVal = row.getElementsByTagName("td")[lastSortedColumn].textContent.trim(), colorStr = "#666";
        if (cellVal !== "-" && lastSortedColumn !== 1 && lastSortedColumn !== 16) {
            let num = parseFloat(cellVal.replace(/[^\d.-]/g, ''));
            if (!isNaN(num)) {
                let vIdx = distinctVals.indexOf(num);
                let revIdx = totalCount - 1 - vIdx; // 0 means highest value, 1 means second highest...

                // Custom low user count logic overrides
                if (totalCount === 1) {
                    colorStr = "hsl(280, 95%, 65%)"; // 1 user: 1 purple
                } else if (totalCount === 2) {
                    colorStr = "hsl(280, 95%, 65%)"; // 2 users: 2 purples
                } else if (totalCount === 3) {
                    if (revIdx < 2) { colorStr = "hsl(280, 95%, 65%)"; } // Top 2 purple
                    else { colorStr = "hsl(0, 95%, 65%)"; }              // Next 1 red
                } else if (totalCount === 4) {
                    if (revIdx < 2) { colorStr = "hsl(280, 95%, 65%)"; } // Top 2 purple
                    else { colorStr = "hsl(0, 95%, 65%)"; }              // Bottom 2 red
                } else if (totalCount === 5) {
                    if (revIdx < 2) { colorStr = "hsl(280, 95%, 65%)"; } // Top 2 purple
                    else if (revIdx === 2) { colorStr = "hsl(20, 95%, 65%)"; } // Middle 1 gets start of gradient
                    else { colorStr = "hsl(0, 95%, 65%)"; }              // Bottom 2 red
                } else {
                    // Standard multi-user gradient engine
                    if (vIdx <= 1) { colorStr = "hsl(0, 95%, 65%)"; }
                    else if (vIdx >= totalCount - 2) { colorStr = "hsl(280, 95%, 65%)"; }
                    else {
                        let steps = totalCount - 4;
                        let stepIdx = vIdx - 2;
                        let factor = steps > 0 ? stepIdx / steps : 0.5;
                        colorStr = `hsl(${factor * 280}, 95%, 65%)`;
                    }
                }
            }
        } else { colorStr = "hsl(280, 95%, 65%)"; }
        row.querySelectorAll("td:not(.name):not(.row-rank):not(:last-child)").forEach(cell => cell.style.color = cell.textContent.trim() !== "-" ? colorStr : "#444");
    });
}
function updateEloCalculations(useVariants) {
    const rows = document.querySelectorAll("#leaderboard-table tbody tr"), formulaTxt = document.getElementById("formula-txt"), eloTh = document.getElementById("elo-th");
    formulaTxt.innerHTML = useVariants ? "<b>Variant ELO = (Crazy+KOTH+3C+Anti+Atomic+Horde+RK) ÷ 7</b>" : "<b>ELO = (Bullet + Blitz + Rapid) ÷ 3</b>";
    eloTh.innerText = useVariants ? "Variant ELO" : "ELO";
    rows.forEach(row => {
        const eloCell = row.querySelector(".elo-cell");
        if (useVariants) {
            let sum = 0, count = 0;
            ["crazy", "koth", "three", "anti", "atomic", "horde", "racing"].forEach(k => {
                let val = row.getAttribute(`data-${k}`);
                if (val !== "") { sum += parseFloat(val); count++; }
            });
            eloCell.innerText = (count > 0) ? Math.round(sum / count) : "-";
        } else { eloCell.innerText = row.getAttribute("data-defaultelo"); }
    });
    sortDirections[2] = true; sortTable(2);
}
function checkCategory(row, category) {
    return category === "sagi-human" ? row.getAttribute("data-sagihuman") === "true" : category === "monster" ? row.getAttribute("data-monster") === "true" : category === "team-bot" ? row.getAttribute("data-teambot") === "true" : category === "external-bot" ? row.getAttribute("data-externalbot") === "true" : false;
}
function hasPlayedVariants(row) { return ["crazy", "koth", "three", "anti", "atomic", "horde", "racing"].some(k => row.getAttribute(`data-${k}`) !== ""); }
function handleCycleClick(buttonElement) {
    const category = buttonElement.getAttribute("data-category"), rows = document.querySelectorAll("#leaderboard-table tbody tr"), formulaBox = document.getElementById("formula-txt");
    let currentState = buttonElement.classList.contains("active-regular") ? 1 : buttonElement.classList.contains("active-variant") ? 2 : buttonElement.classList.contains("active-online") ? 3 : buttonElement.classList.contains("active-variant-online") ? 4 : 0;
    document.querySelectorAll(".legend-item").forEach(btn => btn.classList.remove("active-regular", "active-variant", "active-online", "active-variant-online"));
    formulaBox.classList.remove("highlight-regular", "highlight-variant", "highlight-online", "highlight-variant-online");
    if (currentState === 0) {
        buttonElement.classList.add("active-regular"); formulaBox.classList.add("highlight-regular");
        rows.forEach(row => row.style.display = (checkCategory(row, category) && row.getAttribute("data-bullet") !== "" && row.getAttribute("data-blitz") !== "" && row.getAttribute("data-rapid") !== "") ? "" : "none");
        updateEloCalculations(false);
    } else if (currentState === 1) {
        buttonElement.classList.add("active-variant"); formulaBox.classList.add("highlight-variant");
        rows.forEach(row => row.style.display = (checkCategory(row, category) && hasPlayedVariants(row)) ? "" : "none");
        updateEloCalculations(true);
    } else if (currentState === 2) {
        buttonElement.classList.add("active-online"); formulaBox.classList.add("highlight-online");
        rows.forEach(row => row.style.display = (checkCategory(row, category) && row.getAttribute("data-online") === "true" && row.getAttribute("data-bullet") !== "" && row.getAttribute("data-blitz") !== "" && row.getAttribute("data-rapid") !== "") ? "" : "none");
        updateEloCalculations(false);
    } else if (currentState === 3) {
        buttonElement.classList.add("active-variant-online"); formulaBox.classList.add("highlight-variant-online");
        rows.forEach(row => row.style.display = (checkCategory(row, category) && row.getAttribute("data-online") === "true" && hasPlayedVariants(row)) ? "" : "none");
        updateEloCalculations(true);
    } else if (currentState === 4) {
        rows.forEach(row => row.style.display = "");
        updateEloCalculations(false);
    }
}
document.addEventListener("DOMContentLoaded", () => { sortDirections[2] = true; sortTable(2); });
</script></body></html>"""

@app.route("/")
def index():
    return render_template_string(HTML, bots=CACHE["data"], fields=FIELDS, updated=CACHE["updated"], loading=CACHE["loading"], progress=CACHE["progress"])

if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 5000)))
