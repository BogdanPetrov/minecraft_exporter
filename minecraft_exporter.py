import sys
import json
import time
from pathlib import Path
from prometheus_client import start_http_server, Gauge


MINECRAFT_DIR = Path(sys.argv[1])
SLEEP_INTERVAL_SEC = int(sys.argv[2])
PORT = int(sys.argv[3])

metrics = {}
start_http_server(PORT)


while True:
    
    stats = {}
    for stats_file in Path(MINECRAFT_DIR, 'saves').glob('*/stats/*.json'):
        with open(stats_file, 'r', encoding='utf8') as f:
            stats[stats_file] = json.loads(f.read())
            
    for k, v in stats.items():
        player = k.stem
        world = k.parent.parent.stem
        for k2, v2 in v['stats'].items():
            for k3, v3 in v2.items():
                metric_name = f"{k2.replace(':', '_')}_{k3.replace(':', '_')}_total"
                if metric_name not in metrics.keys():
                    metrics[metric_name] = Gauge(metric_name, '', ['world', 'player'])
                metrics[metric_name].labels(world=world, player=player).set(v3)
                
    time.sleep(SLEEP_INTERVAL_SEC)
