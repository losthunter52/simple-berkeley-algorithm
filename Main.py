from bin import Settings
from bin.Clock import LogicalClock
from bin.Data import Database
from bin.Master import MasterReceptor
from bin.Slave import PassiveReceptor

# ---------------------------------------------------------------------------
# Main Class
# ---------------------------------------------------------------------------

# main method
def Main():
    # responsible for starting and ending the node
    data = Database()
    threads = []

    # init threads
    if Settings.MODEL_LEVEL == 'MASTER':
        master = MasterReceptor()
        threads.append(master)
        master.start()
    slave = PassiveReceptor(data)
    threads.append(slave)
    slave.start()
    clock = LogicalClock(data)
    threads.append(clock)
    clock.start()

    # join threads
    for thread in threads:
        thread.join()


# program launcher
if __name__ == '__main__':
    Main()
