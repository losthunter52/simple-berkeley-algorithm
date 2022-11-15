# Berkeley's Simplified Algorithm

this program emulates the berkeley's algorithm in a simple way

## Running the program

just config /bin/Settings.py params to run the project

```bash
    [...]
    # settings------------------------------------------------------------

        # the SELF_IP parameter defines the IP of this node.
        SELF_IP = '192.168.3.12'

        # the MASTER_IP parameter defines the IP of master node.
        MASTER_IP = '192.168.3.12'

        # the clear_type parameter define the terminal clear command.
        # Use 'cls' for Windows or 'clear' for UNIX.
        CLEAR_TYPE = 'cls'

        # the address_list parameter defines the known network addresses.
        ADDRESS_LIST = [
            '192.168.3.12',
            '192.168.126.131',
        ]

        # the model_level parameter accepts 'MASTER' or 'SLAVE' and sets the
        # role permissions of this node.
        MODEL_LEVEL = 'MASTER'

        # the CLOCK_PARAMS parameter is a dictionary integers that defines the 
        # clock settings.
        CLOCK_PARAMS = {
            # the MODE parameter accepts 'REAL' or 'FAKE' and sets the
            # clock's operating mode.
            'MODE': 'FAKE',
            # the SYNC_INTERVAL parameter accepts integers that define the interval
            # (seconds) in which the clock will be regulated.
            'SYNC_INTERVAL': 5,
            # the COUNT parameter accepts integers that define the interval 
            # (seconds) in which the clock will be deregulated (only on 'FAKE' Mode).
            'CONFUSION_INTERVAL': 18,
            # the CONFUSION_RANGE parameter accepts
            'CONFUSION_RANGE': 3,   
        }

    # ------------------------------------------------------------------
    [...]
```