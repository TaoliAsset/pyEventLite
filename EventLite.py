class EventHandle(object):
    def __init__(self, eventLite, event):
        self.eventLite = eventLite
        self.event = event

    def handleOn(self, fn):
        self.eventLite.on(self.event, fn)
        return self

    def handleOnce(self, fn):
        self.eventLite.on(self.event, fn)
        return self

    def handleEmit(self, *args):
        self.eventLite.emit(self.event, *args)
        return self

    def handleRemove(self, fn=None):
        self.eventLite.remove(self.event, fn)
        return self

    def handleConnect(self, eventLite=None):
        self.eventLite.connect(self.event, eventLite)
        return self


class EventLite(object):
    def __init__(self):
        self.doMap = dict()
        self.doOnceMap = dict()

    def on(self, event, fn):
        map = self.doMap
        if not map.get(event):
            map[event] = {fn}
        else:
            map[event].add(fn)

        return self.handle(event)

    def once(self, event, fn):
        map = self.doOnceMap
        if not map.get(event):
            map[event] = {fn}
        else:
            map[event].add(fn)

        return self.handle(event)

    def emit(self, event, *args):

        dos = self.doMap.get(event)
        if dos:
            for fn in dos:
                fn(*args)

        doOnces = self.doOnceMap.get(event)
        if doOnces:
            for fn in doOnces:
                fn(*args)
            del self.doOnceMap[event]

        return self.handle(event)

    def remove(self, event=None, fn=None):
        if event and fn:
            dos = self.doMap.get(event)
            if dos:
                dos.add(fn)
                dos.remove(fn)

            dos = self.doOnceMap.get(event)
            if dos:
                dos.add(fn)
                dos.remove(fn)

        elif event:
            dos = self.doMap.get(event)
            if dos:
                dos.clear()

            dos = self.doOnceMap.get(event)
            if dos:
                dos.clear()

        elif fn:
            for dos in self.doMap.values():
                dos.add(fn)
                dos.remove(fn)

            for dos in self.doOnceMap.values():
                dos.add(fn)
                dos.remove(fn)

        return self

    def connect(self, event, eventLite=None):
        if not eventLite:
            eventLite = EventLite()

        def socket(*args):
            eventLite.emit(event, *args)
            pass

        self.on(event, socket)

        return eventLite.handle(event)

    def handle(self, event):
        # print(make)
        return EventHandle(self, event)


if __name__ == "__main__":
    eventLite = EventLite()

    def eatApple(*args):
        print("eatApple", *args)

    def drinkWater(*args):
        print("drinkWater", *args)

    print("add")
    eventLite.on("eat", eatApple)
    eventLite.once("drink", drinkWater)

    print("do 1")
    eventLite.emit("eat", 1)
    eventLite.emit("drink", 2)

    print("do 2")
    eventLite.emit("eat")
    eventLite.emit("drink", 4)

    print("remove")
    eventLite.on("eat", drinkWater)
    eventLite.once("eat", drinkWater)
    eventLite.remove("eat")

    print("after remove")
    eventLite.emit("eat", 5)
    eventLite.emit("drink", 6)

    print("remove")
    eventLite.on("eat", drinkWater)
    eventLite.once("drink", drinkWater)
    eventLite.remove("", drinkWater)

    print("after remove")
    eventLite.emit("eat", 7)
    eventLite.emit("drink")

    print("handle")
    eat = eventLite.handle("eat")
    drink = eventLite.handle("drink")

    eat.handleOn(eatApple)
    eat.handleEmit().handleEmit()

    print("connect")
    connectEat = eventLite.connect("eat")

    connectEat.handleOn(eatApple)
    eat.handleEmit(10).handleEmit(11)
