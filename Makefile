.PHONY: clean check

check:
	pychecker2 *.py

clean:
	find . -name "*~" -print0 | xargs -0 rm -f
	find . -name "*.pyc" -print0 | xargs -0 rm -f


