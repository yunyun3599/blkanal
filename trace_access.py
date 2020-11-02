import trace_data
import trace_context
import access

class TraceAccess(trace_data.TraceData):
    def __init__(self, args):
        super().__init__()
        self.accesses = []
        self.accesses_read = []
        self.accesses_write = []
        self.contexts = {}
        self.lba_min = -1
        self.lba_max = 0
        self.__args = args

    def parseLine(self, row):
        acc = access.Access(row)
        if acc.lba < self.__args.lba_start or (self.__args.lba_end > 0 and acc.lba > self.__args.lba_end):
            return
        if acc.ts < self.__args.ts_start or acc.ts > self.__args.ts_end:
            return
        if acc.is_read is None:
            return
        if self.__args.pidonly >= 0:
            if self.__args.pidonly != acc.pid:
                return

        if self.__args.writeonly:
            if acc.is_read:
                return
        if self.__args.readonly:
            if not acc.is_read:
                return
        if self.lba_min < 0 or acc.lba < self.lba_min:
            self.lba_min = acc.lba
        if acc.lba > self.lba_max:
            self.lba_max = acc.lba

        ctx = trace_context.TraceContext(row)
        if ctx in self.contexts:
            acc.context = self.contexts[ctx]
        else:
            self.contexts[ctx] = ctx
            acc.context = ctx

        acc.context.add(acc)
        acc.setLbaDiff(self.accesses[-1 * self.__args.n_lookbacks:])
        self.accesses.append(acc)
        if acc.is_read:
            self.accesses_read.append(acc)
        else:
            self.accesses_write.append(acc)

    def summary(self):
        print("access count: {}(read:{}, write:{})".format(len(self.accesses), len(self.accesses_read), len(self.accesses_write)))
        print("LBA: {}-{}".format(self.lba_min, self.lba_max))
        print("timestamp: {}-{}".format(format(self.accesses[0].ts, ".4f"), format(self.accesses[-1].ts, ".4f")))
        for c in self.contexts:
            print(c)
