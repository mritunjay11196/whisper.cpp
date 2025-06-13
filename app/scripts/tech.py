objects = ["rectangle", "circle", "donut", "ellipse", "path"]

params = ["name", "width", "height", "fingers"]

instances = ["nmos", "pmos"]

layers = [f"metal {i}" for i in range(1, 10)] + \
         [f"via {i}" for i in range(1, 9)] + \
         ["nwell", "oxide", "oxide_thk", "poly", "pimp", "SNA"]

purposes = ["drawing", "IO", "slot", "pin", "net", "label", "boundary"]