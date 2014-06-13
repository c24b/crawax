#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
run.py
Check the project inside the task manager and launch a crawl
according to configuration and the last date of run
"""
#!/usr/bin/env python
# -*- coding: utf-8 -

from manager import Jobs

if __name__ == "__main__":
	j = Jobs()
	print j.__repr__()
	#print j.cron()
