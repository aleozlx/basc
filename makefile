testbasc:
	@echo =[PARSE]==============
	@python basc.py example/sumassert.bas --parse
	@echo =[COMPILE]============
	@python basc.py example/sumassert.bas

testgotoc:
	@echo =[PARSE]==============
	@python basc.py example/sumassert.bas --parse
	@echo =[COMPILE]============
	@python basc.py --goto example/sumassert.bas

examples:
	mkdir debug -p
	python basc.py example/hello.bas > debug/hello.py
	python basc.py example/countdown.bas > debug/countdown.py
	python basc.py example/sumassert.bas > debug/sumassert.py

clean:
	rm -R debug

