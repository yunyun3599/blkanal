from accbmpcol import AccBmpCol
from accbmp import AccBmp
from acchist import AccessHist
import conf

class AccBmpBar:
    def __init__(self, lba_max, accesses):
        if conf.lba_max == 0:
            self.lbamax = lba_max
        else:
            self.lbamax = conf.lba_max
        self.__bmp_cols = []
        self.__build(accesses)

    def __build(self, accesses):
        if len(accesses) == 0:
            return

        acchist = AccessHist(conf.ts_intv * conf.width)

        ts_start = int(accesses[0].ts / conf.ts_intv) * conf.ts_intv
        ts_end = ts_start + conf.ts_intv
        bmp_col = AccBmpCol(self.lbamax, conf.height)

        for acc in accesses:
            accbit = acchist.append(acc)
            while acc.ts >= ts_end:
                ts_start = ts_end
                ts_end += conf.ts_intv
                self.__bmp_cols.append(bmp_col)
                bmp_col = AccBmpCol(self.lbamax, conf.height)
            bmp_col.setBitByLba(acc.lba, accbit)

        if not bmp_col.is_empty:
            self.__bmp_cols.append(bmp_col)

    def __iter__(self):
        self.__index = 0
        return self

    def __next__(self):
        while True:
            if self.__index >= len(self.__bmp_cols) - conf.width:
                raise StopIteration

            acc_bmp = AccBmp(conf.width, conf.height)
            for i in range(self.__index, self.__index + conf.width):
                if i < len(self.__bmp_cols):
                    acc_bmp.append(self.__bmp_cols[i])
                else:
                    acc_bmp.append(None)
            self.__index += 1
            if acc_bmp.is_valid():
                idx_forward = self.__index + conf.width - 1
                acc_bmp.bmpcol_forwards = self.__bmp_cols[idx_forward:idx_forward + conf.n_forwards - 1]
                acc_bmp.calcScore()
                if acc_bmp.score.count > 0:
                    return acc_bmp
