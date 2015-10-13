Productivity Tracker
====================

Since I began working, I've been curious about how much work I do, and when am I most productive. Having used an Amazon Dash button for a previous project, I felt it would be perfect to measure how much time I've been at my desk, and the relative productiveness based on keypresses.

This script uses a package manipulation tool called Scapy to detect the ARP probes sent out from the AmazonDash button. On press, the script starts a subprocess that will run a key logger to return the number of key presses until the next press.

The key logger listens to all keypresses in OS X through the Cocoa API using Python and PyObjC. The handler increments a counter variable that is returned once the 'SIGUSR1' is sent, through the output pipe.

Once returned the Google Form is updated using a service called Cloudstitch.

![Productivity Tracker Sheet](http://i.imgur.com/JmHGY1Y.png)

## References

* Thanks goes to Ted Benson and his great [tutorial](https://medium.com/@edwardbenson/how-i-hacked-amazon-s-5-wifi-button-to-track-baby-data-794214b0bdd8) to get started
* The awesome ~25 line key logger I used was from [Bjarte Johansen](https://gist.github.com/ljos/3019549)
