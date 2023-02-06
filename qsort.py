import os
from time import sleep


class QSortMedianThree:

    def __init__(self):
        self._COMP_FXNS = {
            'action_queue': self._action_queue_comparator
        }

    @staticmethod
    def _action_queue_comparator(a, b):
        return a - b

    def qsort_median_of_three(self, keylist, sortlist, comparator='action_queue'):
        """Returns the keylist and sortlist as sorted by the sortlist from low to high"""

        if len(keylist) != len(sortlist):
            raise IndexError('key list and sort list have different lengths. Cannot sort key list using sort list')

        if len(keylist) < 2:
            return keylist

        count: int = len(sortlist)

        # The following code was adapted from the Ghidra decompilation of SOAL 8025eb4c

        # For debugging vs SOAL:
        # count -> register 27

        uVar8: int = (count >> 1) + 1
        pMidpoint: int = count >> 1
        pEnd: int = count - 1
        while True:
            if uVar8 < 2:
                s_uVar1 = sortlist[pMidpoint]
                k_uVar1 = keylist[pMidpoint]

                sortlist[pMidpoint] = sortlist[pEnd]
                keylist[pMidpoint] = keylist[pEnd]

                sortlist[pEnd] = s_uVar1
                keylist[pEnd] = k_uVar1

                count -= 1
                if count == 1:
                    return keylist, sortlist
                pEnd -= 1

            else:
                pMidpoint -= 1
                uVar8 -= 1

            pvVar6: int = uVar8 - 1
            uVar7: int = uVar8
            compare = uVar7 << 1
            while compare <= count:  # 8025ec98 -> 8025eca0
                uVar7 *= 2
                pvVar5: int = uVar7 - 1
                if uVar7 < count:
                    iVar2 = self._COMP_FXNS[comparator](sortlist[pvVar5], sortlist[pvVar5 + 1])
                    if iVar2 < 0:
                        uVar7 += 1
                        pvVar5 += 1

                iVar2 = self._COMP_FXNS[comparator](sortlist[pvVar6], sortlist[pvVar5])
                if -1 < iVar2:
                    break
                iVar2 = pvVar5
                iVar3 = pvVar6

                s_uVar1 = sortlist[iVar3]
                k_uVar1 = keylist[iVar3]

                sortlist[iVar3] = sortlist[iVar2]
                keylist[iVar3] = keylist[iVar2]

                sortlist[iVar2] = s_uVar1
                keylist[iVar2] = k_uVar1

                pvVar6 = pvVar5
                compare = uVar7 << 1


sort_dict = {}
klist_in = []
slist_in = []


def populate_sortlists():
    global sort_dict
    global klist_in
    global slist_in
    klist_in = []
    slist_in = []
    for i in range(12):
        if i in sort_dict.keys():
            klist_in.append(i)
            slist_in.append(sort_dict[i])


def main():
    qsort = QSortMedianThree()

    print('Welcome to the Skies of Arcadia combatant sort simulator.')
    global sort_dict
    global slist_in
    global klist_in

    state = 0
    while True:
        if state == 0:
            i = input('Please select one of the following options:\n(1) Start a simulation\n(2) Quit\n')
            if i not in ('1', '2'):
                print('Invalid selection')
                sleep(1)
                os.system('cls')
                continue
            if i == 2:
                break
            state = 1

        if state == 1:
            os.system('cls')
            print('\nCurrent combatant array:')
            for i in range(len(klist_in)):
                print(f'  id:\t{klist_in[i]}\t-\t{slist_in[i]}')
            i = input('\nPlease select one of the following options:\n(1) Add a combatant\n(2) Modify a combatant\n(3) Remove a combatant\n(4) Run Simulation\n(5) Quit\n')
            if i not in ('1', '2', '3', '4'):
                print('\nInvalid selection')
                sleep(1)
                continue
            if i == '5':
                break
            elif i == '2':
                if len(klist_in) == 0:
                    print('No combatants present, unable to modify a  combatant')
                    sleep(1)
                    continue
                j = input('\nWhich combatant would you like to modify?\n')
                if not j.isnumeric():
                    print('\nInvalid selection, please enter a number between 0 and 11 inclusive')
                    sleep(1)
                    continue
                j = int(j)
                if j not in sort_dict.keys():
                    print(f'\nInvalid selection, {j} is not a current combatant')
                    sleep(1)
                    continue
                while True:
                    s = input(f'\nPlease enter the adjustedQuick value for {j}:\n')
                    if not s.isnumeric():
                        print('\nInvalid selection')
                        sleep(1)
                        continue
                    s = int(s)
                    if 0 > s:
                        print(f'\nInvalid entry: {s} is less than zero')
                        sleep(1)
                        continue
                    break
                sort_dict[j] = s
                populate_sortlists()

            elif i == '3':
                if len(klist_in) == 0:
                    print('\nNo combatants present, unable to remove combatant')
                    sleep(1)
                    continue
                j = input('\nWhich combatant would you like to remove?\n')
                if not j.isnumeric():
                    print('\nInvalid selection')
                    sleep(1)
                    continue

                j = int(j)
                if j in sort_dict.keys():
                    sort_dict.pop(j)
                    populate_sortlists()
                else:
                    print(f'Invalid selection: {j} is not a current combatant')
                    sleep(1)
                    continue
            elif i == '1':
                k = input('Please enter the combatantID (0 ~ 11):\n')
                if not k.isnumeric():
                    print('Invalid selection')
                    sleep(1)
                    continue
                k = int(k)
                if k in klist_in:
                    print(f'Invalid selection: {k} is already added')
                    sleep(1)
                    continue
                if not (-1 < k < 12):
                    print(f'Invalid selection: {k} is out of the range of potential combatantIDs ( 0 ~ 11 )')
                    sleep(1)
                    continue

                while True:
                    s = input(f'Please enter the adjustedQuick value for {k}:\n')
                    if not s.isnumeric():
                        print('Invalid selection')
                        sleep(1)
                        continue
                    s = int(s)
                    if 0 > s:
                        print(f'Invalid entry: {s} is less than zero')
                        sleep(1)
                        continue
                    break
                sort_dict[k] = s
                populate_sortlists()
            else:
                if len(sort_dict) < 2:
                    print(f'Unable to sort less than 2 combatants')
                    sleep(1)
                    continue
                state = 2

        if state == 2:
            method = 'action_queue'
            klist_out, slist_out = qsort.qsort_median_of_three(keylist=klist_in.copy(), sortlist=slist_in.copy(),
                                                               comparator=method)
            print(f'\nLists sorted:\nInput:\t{klist_in}\n\t\t{slist_in}\nOutput:\t{klist_out}\n\t\t{slist_out}')
            while True:
                l = input('\nPlease select one of the following options:\n(1) Start new array\n(2) Modify previous array\n(3) Quit\n')
                if l not in ('1', '2', '3'):
                    print(f'\nInvalid selection', end='\r')
                    sleep(1)
                    continue
                break
            if l == '3':
                break
            if l == '1':
                sort_dict = {}
                populate_sortlists()
            state = 1


if __name__ == '__main__':
    main()
