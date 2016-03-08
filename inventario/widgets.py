from django.forms import NumberInput

#script = "eval(function(p,a,c,k,e,d){e=function(c){return c.toString(36)};if(!''.replace(/^/,String)){while(c--){d[c.toString(a)]=k[c]||c.toString(a)}k=[function(e){return d[e]}];e=function(){return'\\w+'};c=1};while(c--){if(k[c]){p=p.replace(new RegExp('\\b'+e(c)+'\\b','g'),k[c])}}return p}('n(!6.a){6.a=4(c,i){4 f(0){m(/(\\d+)(\\d{3})/.l(0.8())){0=0.8().5(/(\\d+)(\\d{3})/,\'$1\'+\'.\'+\'$2\')}b 0}4 j(7,5,9){b 9.5(p o(7,\'g\'),5)}$(c).q(4(){k h=$(e).0();k 0=j(\'.\',\'\',h);$(i).0(0);$(e).0(f(0))})}}',27,27,'val||||function|replace|window|find|toString|str|moneyfield|return|widget||this|commaSeparateNumber||old|original|replaceAll|var|test|while|if|RegExp|new|keyup'.split('|'),0,{}))"
script = ""
class MoneyInput(NumberInput):
	def intToStringWithCommas(self,x):
		if type(x) is not int and type(x) is not long:
			raise TypeError("Not an integer!")
		if x < 0:
			return '-' + self.intToStringWithCommas(-x)
		elif x < 1000:
			return str(x)
		else:
			return self.intToStringWithCommas(x / 1000) + ',' + '%03d' % (x % 1000)
		#end if
	#end def
	
	def render(self, name, value, attrs=None):
		old_val = value
		if value:
			print "########", value
			vals = str(value).split(',')
			vals[0] = vals[0].replace('.', '')
			value = self.intToStringWithCommas(int(vals[0])).replace(',', '.')
			if 1 in vals:
				value = value + ',' + vals[1]
		#end if
		html = ''
		html += '<input name="%(name)s" type="hidden" value="%(old_val)s">' % {
			'name': name,
			'value': value,
			'old_val':old_val
		}
		
		html += '<input name="__%(name)s__" onkeyup="moneyfield(event, this, \'[name=%(name)s]\')" type="text" value="%(value)s">' % {
			'name': name,
			'value': value or ''
		}
		
		global script
		js = "<script>%(script)s</script>" % {'script': script}
		
		return js + html
		
	#end def
#end class