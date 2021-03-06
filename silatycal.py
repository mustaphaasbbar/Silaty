from gi.repository import GObject, GLib, Gtk, Gdk, GdkPixbuf
from datetime import date, timedelta
from hijrical import *
import datetime
import os

class SilatyCal(Gtk.Box):
	def __init__(self):
		Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=12, margin_bottom=12)

		#Set the Date in the Title
		topbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, halign=Gtk.Align.FILL, margin_right=0, margin_left=12, margin_top=12, margin_bottom=12)
		self.titlestack = Gtk.Stack()
		self.titlestack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)
		self.titlestack.set_transition_duration(300)
		self.titlestack.set_halign = Gtk.Align.START

		now_wd=datetime.datetime.now().strftime("%A")
		
		g_date=datetime.datetime.now().strftime("%d %B %Y")
		gtitlelabel = Gtk.Label(label=(now_wd+", "+g_date))
		gtitlelabel.props.halign = Gtk.Align.START
		
		calc = HijriCal()
		h_months = ['Muharram', 'Safar', 'Rabi al Awwal', 'Rabi al Akhira', 'Jumada al Ula', 'Jumada al Akhira', 'Rajab',  "Sha'ban",  'Ramadan',  'Shawwal',  "Dhu al Qa'da", 'Dhu al Hijja']
		h_year,  h_month,  h_day,  h_week_day = calc.today
		h_date = '%i %s %i' % ( h_day,  h_months[int(h_month-1)],  h_year)
		htitlelabel = Gtk.Label(label=(now_wd+", "+h_date))
		htitlelabel.props.halign = Gtk.Align.START

		self.titlestack.add_named(gtitlelabel, "Gregorian")
		self.titlestack.add_named(htitlelabel, "Hijri")
		
		topbox.pack_start(self.titlestack , False, False, 0)

		#Set up the Hijri/Gregorian Switch
		hijrilabel = Gtk.Label('Hijri:', halign=Gtk.Align.START)
		self.hijri = Gtk.Switch(halign=Gtk.Align.END)
		self.hijri.set_active(False)
		self.hijri.connect('button-press-event', self.on_entered_hijri)
		hijrilabel.set_halign(Gtk.Align.START)
		
		box= Gtk.Box(halign=Gtk.Align.END, spacing=6)
		box.pack_start(hijrilabel, False, True, 0)
		box.pack_start(self.hijri, False, False, 0)
		topbox.pack_end(box, False, False, 0)

		#Set up the date switcher
		self.cal = Cal()

		
		#bottombox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, halign=Gtk.Align.FILL, margin=24)
		#opmaya = Gtk.Button(label="Open Maya")
		#datesettings = Gtk.Button(label="Date and Time settings")

		#bottombox.pack_start(opmaya, False, False, 0)
		#bottombox.pack_end(datesettings, False, False, 0)


		self.pack_start(topbox, False, True, 0)
		self.pack_start(self.cal, False, False, 0)
		#self.pack_start(bottombox, False, True, 0)

	def on_entered_hijri(self, widget, event):
		if not(widget.get_active()) == True:
			self.cal.state = State.Hijri
			self.titlestack.set_visible_child_name("Hijri")
			for row in range(0, 6):
				for column in range(0, 7):				
						self.cal.caltable.get_child_at(column,row).state = State.Hijri
		else:
			self.cal.state = State.Gregorian
			self.titlestack.set_visible_child_name("Gregorian")
			for row in range(0, 6):
				for column in range(0, 7):				
						self.cal.caltable.get_child_at(column,row).state = State.Gregorian

class Cal(Gtk.Box):
	def __init__(self):
		Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=12)
		self.dateswitcher = Gtk.Grid(row_homogeneous=True)
		self.dateswitcher.set_halign(Gtk.Align.CENTER)

		self._refdate = datetime.datetime.today()
		self.hijcal = HijriCal()
		self.weekdays = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
		self.gmonths = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
		self.hmonths = ['Muharram', 'Safar', 'Rabi al Awwal', 'Rabi al Akhira', 'Jumada al Ula', 'Jumada al Akhira', 'Rajab',  "Sha'ban",  'Ramadhan',  'Shawwal',  "Dhu al Qa'da", 'Dhu al Hijja']
		self._state = State.Gregorian

		self.gmonthstack = Gtk.Stack()
		self.gmonthstack.set_transition_duration(300)
		self.gmonthstack.set_homogeneous(True)

		self.gmonthstack.add_named(Gtk.Label(label="January",   name="Label"), "January")
		self.gmonthstack.add_named(Gtk.Label(label="February",  name="Label"), "February")
		self.gmonthstack.add_named(Gtk.Label(label="March",     name="Label"), "March")
		self.gmonthstack.add_named(Gtk.Label(label="April",     name="Label"), "April")
		self.gmonthstack.add_named(Gtk.Label(label="May",       name="Label"), "May")
		self.gmonthstack.add_named(Gtk.Label(label="June",      name="Label"), "June")
		self.gmonthstack.add_named(Gtk.Label(label="July",      name="Label"), "July")
		self.gmonthstack.add_named(Gtk.Label(label="August",    name="Label"), "August")
		self.gmonthstack.add_named(Gtk.Label(label="September", name="Label"), "September")
		self.gmonthstack.add_named(Gtk.Label(label="October",   name="Label"), "October")
		self.gmonthstack.add_named(Gtk.Label(label="November",  name="Label"), "November")
		self.gmonthstack.add_named(Gtk.Label(label="December",  name="Label"), "December")

		self.hmonthstack = Gtk.Stack()
		self.hmonthstack.set_transition_duration(300)
		self.hmonthstack.set_homogeneous(True)

		self.hmonthstack.add_named(Gtk.Label(label="Muharram",         name="Label"), "Muharram")
		self.hmonthstack.add_named(Gtk.Label(label="Safar",            name="Label"), "Safar")
		self.hmonthstack.add_named(Gtk.Label(label="Rabi al Awwal",    name="Label"), "Rabi al Awwal")
		self.hmonthstack.add_named(Gtk.Label(label="Rabi al Akhira",   name="Label"), "Rabi al Akhira")
		self.hmonthstack.add_named(Gtk.Label(label="Jumada al Ula",    name="Label"), "Jumada al Ula")
		self.hmonthstack.add_named(Gtk.Label(label="Jumada al Akhira", name="Label"), "Jumada al Akhira")
		self.hmonthstack.add_named(Gtk.Label(label="Rajab",            name="Label"), "Rajab")
		self.hmonthstack.add_named(Gtk.Label(label="Sha'ban",          name="Label"), "Sha'ban")
		self.hmonthstack.add_named(Gtk.Label(label="Ramadhan",         name="Label"), "Ramadhan")
		self.hmonthstack.add_named(Gtk.Label(label="Shawwal",          name="Label"), "Shawwal")
		self.hmonthstack.add_named(Gtk.Label(label="Dhu al Qa'da",     name="Label"), "Dhu al Qa'da")
		self.hmonthstack.add_named(Gtk.Label(label="Dhu al Hijja",     name="Label"), "Dhu al Hijja")

		self.combinedstack = Gtk.Stack()
		self.combinedstack.set_transition_type(Gtk.StackTransitionType.SLIDE_UP_DOWN)
		self.combinedstack.set_transition_duration(200)
		self.combinedstack.set_homogeneous(True)

		self.combinedstack.add_named(self.gmonthstack, "Gregorian")
		self.combinedstack.add_named(self.hmonthstack, "Hijri")

		lefticon = os.path.dirname(os.path.realpath(__file__)) + "/icons/arrows/arrow-left.svg"
		leftarrow = self.set_image_from_file(lefticon)
		leftbox = Gtk.EventBox()
		leftbox.set_events(Gdk.EventMask.BUTTON_PRESS_MASK)
		leftbox.add(leftarrow)
		
		righticon = os.path.dirname(os.path.realpath(__file__)) + "/icons/arrows/arrow-right.svg"
		rightarrow = self.set_image_from_file(righticon)
		rightbox = Gtk.EventBox()
		rightbox.set_events(Gdk.EventMask.BUTTON_PRESS_MASK)
		rightbox.add(rightarrow)

		self.dateswitcher.attach(leftbox, 0, 0, 1, 1)
		self.dateswitcher.attach(self.combinedstack, 1, 0, 1, 1)
		self.dateswitcher.attach(rightbox, 2, 0, 1, 1)

		leftbox.connect("button-press-event", self.left_arrow_pressed)
		rightbox.connect("button-press-event", self.right_arrow_pressed)

		self.dateswitcher.set_name('Switcher')
		leftarrow.set_name('LeftArrow')
		rightarrow.set_name('RightArrow')

		css = b"""
			#Switcher{
				background-color: white;
				box-shadow: 0 0 3px #333 inset;
				border-radius: 3px;
			}

			#LeftArrow{
				padding-left: 6px;
			}

			#Label{
				padding-left: 24px;
				padding-right: 24px;
				padding-top: 4px;
				padding-bottom: 4px;
			}

			#RightArrow{
				padding-right: 6px;
			}
		"""

		style_provider = Gtk.CssProvider()

		style_provider.load_from_data(css)

		Gtk.StyleContext.add_provider_for_screen(
			Gdk.Screen.get_default(),\
			style_provider,\
			Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
		)

		self.pack_start(self.dateswitcher, False, False, 0)
		self.show_all()
		gday   = (self.refdate).strftime("%d")
		gmonth = (self.refdate).strftime("%B")
		gyear  = (self.refdate).strftime("%Y")		
		hyear, hmonth, hday = self.hijcal.goto_gregorian_day(int(gyear), (self.gmonths.index(gmonth)+1), int(gday))

		self.gmonthstack.set_visible_child_name(self.refdate.strftime("%B"))
		self.hmonthstack.set_visible_child_name(self.hmonths[int(hmonth-1)])

		self.calbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		self.calbox.set_halign(Gtk.Align.CENTER)
		
		#Label for the weekdays
		wkgrid = Gtk.Grid(row_homogeneous=True, column_homogeneous=True, row_spacing=2, column_spacing=2)
		wkgrid.set_border_width(2)

		wklabel = Gtk.Label(label="S")
		wklabel.set_size_request(34,26)
		wkgrid.attach(wklabel, 0, 0, 1, 1)

		wklabel = Gtk.Label(label="M")
		wklabel.set_size_request(34,26)
		wkgrid.attach(wklabel, 1, 0, 1, 1)

		wklabel = Gtk.Label(label="T")
		wklabel.set_size_request(34,26)
		wkgrid.attach(wklabel, 2, 0, 1, 1)

		wklabel = Gtk.Label(label="W")
		wklabel.set_size_request(34,26)
		wkgrid.attach(wklabel, 3, 0, 1, 1)

		wklabel = Gtk.Label(label="T")
		wklabel.set_size_request(34,26)
		wkgrid.attach(wklabel, 4, 0, 1, 1)

		wklabel = Gtk.Label(label="F")
		wklabel.set_size_request(34,26)
		wkgrid.attach(wklabel, 5, 0, 1, 1)

		wklabel = Gtk.Label(label="S")
		wklabel.set_size_request(34,26)
		wkgrid.attach(wklabel, 6, 0, 1, 1)

		self.calbox.pack_start(wkgrid, False, False, 0)

		tablebox = Gtk.Box(halign=Gtk.Align.CENTER, valign=Gtk.Align.CENTER)
		color = 200.0/256.0
		tablebox.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA.from_color(Gdk.Color.from_floats(color,color,color)))		
		self.caltable = Gtk.Grid(row_homogeneous=True, column_homogeneous=True, row_spacing=1, column_spacing=1)
		self.caltable.set_halign(Gtk.Align.CENTER)
		self.caltable.set_valign(Gtk.Align.CENTER)
		self.caltable.set_border_width(1)
		self.caltable.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA.from_color(Gdk.Color.from_floats(color,color,color)))
		tablebox.add(self.caltable)
		self.calbox.pack_start(tablebox, True, True, 0)

		_gday   = datetime.datetime.now().strftime("%d")
		_gmonth = datetime.datetime.now().strftime("%B")
		_gyear  = datetime.datetime.now().strftime("%Y")		
		_gwd    = datetime.datetime.now().strftime("%A")

		wtoday = self.weekdays.index(_gwd)
		self.gdtoday = int(_gday)
		self.gmtoday = self.gmonths.index(_gmonth)
		self.gytoday = int(_gyear)

		hijrical = HijriCal()

		self.hytoday, self.hmtoday, self.hdtoday = hijrical.goto_gregorian_day(self.gytoday, (self.gmtoday+1), self.gdtoday)

		calendarindex = -(wtoday+(((6-wtoday)+self.gdtoday)//7)*7)
		
		for row in range(0, 6):
			for column in range(0, 7):				
				if (column == 0) or (column == 6):
					gcolor = Color.LGrey
					hcolor = Color.LGrey
				else:
					gcolor = Color.White
					hcolor = Color.White

				cgdday = int((datetime.datetime.now() + timedelta(days=calendarindex)).strftime("%d"))
				cgmday = self.gmonths.index((datetime.datetime.now() + timedelta(days=calendarindex)).strftime("%B"))
				cgyday = int((datetime.datetime.now() + timedelta(days=calendarindex)).strftime("%Y"))

				chyday, chmday, chdday = hijrical.goto_gregorian_day(cgyday, (cgmday+1), cgdday)

				if (cgmday != self.gmtoday):
					gcolor = Color.DGrey
				
				if (cgdday == self.gdtoday and cgmday == self.gmtoday and cgyday == self.gytoday):
					gcolor = Color.Blue

				if (chmday != self.hmtoday):
					hcolor = Color.DGrey

				if (chdday == self.hdtoday and chmday == self.hmtoday and chyday == self.hytoday):
					hcolor = Color.Blue

				entry = CalEntry(cgdday, chdday, gcolor, hcolor)
				self.caltable.attach(entry,column,row,1,1)
				
				calendarindex += 1

		self.pack_start(self.calbox, True, True, 0)

	@property
	def state(self):
		return self._state
		
	@state.setter
	def state(self, value):
		if value == State.Hijri:
			self.combinedstack.set_visible_child_name('Hijri')
		else:
			self.combinedstack.set_visible_child_name('Gregorian')
		self._state = value

	@property
	def refdate(self):
	    return self._refdate
	
	@refdate.setter
	def refdate(self, value):
	    self._refdate = value

	def left_arrow_pressed(self, widget, event):
		if self.state == State.Gregorian:
			#Get the size of previous month
			first = datetime.date(day=1, month=self.refdate.month, year=self.refdate.year)
			ndays = int((first - datetime.timedelta(days=1)).strftime("%d"))
			self.refdate = self.refdate - datetime.timedelta(days=ndays)
			gday   = self.refdate.strftime("%d")
			gmonth = self.refdate.strftime("%B")
			gyear  = self.refdate.strftime("%Y")
			hyear, hmonth, hday = self.hijcal.goto_gregorian_day(int(gyear), (self.gmonths.index(gmonth)+1), int(gday))
			refwd = self.weekdays.index(self.refdate.strftime("%A"))
			calendarindex = -(refwd+(((6-refwd)+int(self.refdate.strftime("%d")))//7)*7)
		else:
			gday   = self.refdate.strftime("%d")
			gmonth = self.refdate.strftime("%B")
			gyear  = self.refdate.strftime("%Y")		
			hyear, hmonth, hday = self.hijcal.goto_gregorian_day(int(gyear), (self.gmonths.index(gmonth)+1), int(gday))
			ndays = hijri_month_days(hyear, hmonth-2)
			self.refdate = self.refdate-timedelta(days=ndays)
			gday   = self.refdate.strftime("%d")
			gmonth = self.refdate.strftime("%B")
			gyear  = self.refdate.strftime("%Y")
			hyear, hmonth, hday = self.hijcal.goto_gregorian_day(int(gyear), (self.gmonths.index(gmonth)+1), int(gday))
			refwd = self.weekdays.index(self.refdate.strftime("%A"))
			calendarindex = -(refwd+(((6-refwd)+hday)//7)*7)
		self.shift_days_of_table(gday, gmonth, gyear, hday, hmonth, hyear, calendarindex, Direction.RIGHT)
		self.gmonthstack.set_visible_child_full(self.refdate.strftime("%B"), Gtk.StackTransitionType.SLIDE_RIGHT)
		self.hmonthstack.set_visible_child_full(self.hmonths[int(hmonth)-1], Gtk.StackTransitionType.SLIDE_RIGHT)

	def right_arrow_pressed(self, widget, event):
		if self.state == State.Gregorian:
			#Get the size of this month
			first = (datetime.date(day=28, month=self.refdate.month, year=self.refdate.year)+timedelta(days=4)).replace(day=1)
			ndays = int((first - datetime.timedelta(days=1)).strftime("%d"))
			self.refdate = self.refdate + datetime.timedelta(days=ndays)
			gday   = (self.refdate).strftime("%d")
			gmonth = (self.refdate).strftime("%B")
			gyear  = (self.refdate).strftime("%Y")
			hyear, hmonth, hday = self.hijcal.goto_gregorian_day(int(gyear), (self.gmonths.index(gmonth)+1), int(gday))
			refwd = self.weekdays.index(self.refdate.strftime("%A"))
			calendarindex = -(refwd+(((6-refwd)+int(self.refdate.strftime("%d")))//7)*7)
		else:
			gday   = (self.refdate).strftime("%d")
			gmonth = (self.refdate).strftime("%B")
			gyear  = (self.refdate).strftime("%Y")
			hyear, hmonth, hday = self.hijcal.goto_gregorian_day(int(gyear), (self.gmonths.index(gmonth)+1), int(gday))
			ndays = timedelta(days=hijri_month_days(hyear, hmonth))
			self.refdate = self.refdate+ndays
			gday   = self.refdate.strftime("%d")
			gmonth = self.refdate.strftime("%B")
			gyear  = self.refdate.strftime("%Y")
			hyear, hmonth, hday = self.hijcal.goto_gregorian_day(int(gyear), (self.gmonths.index(gmonth)+1), int(gday))
			refwd = self.weekdays.index(self.refdate.strftime("%A"))
			calendarindex = -(refwd+(((6-refwd)+hday)//7)*7)			
		self.shift_days_of_table(gday, gmonth, gyear, hday, hmonth, hyear, calendarindex, Direction.LEFT)
		self.gmonthstack.set_visible_child_full(self.refdate.strftime("%B"), Gtk.StackTransitionType.SLIDE_LEFT)
		self.hmonthstack.set_visible_child_full(self.hmonths[int(hmonth)-1], Gtk.StackTransitionType.SLIDE_LEFT)

	def set_image_from_file(self, iconpath):
		try:
			pixbuf = GdkPixbuf.Pixbuf.new_from_file(iconpath)
			icon = Gtk.Image.new_from_pixbuf(pixbuf)
		except GLib.GError:
			icon = Gtk.Image.new_from_stock(Gtk.STOCK_MISSING_IMAGE, 22)
		return icon


	def shift_days_of_table(self, gday, gmonth, gyear, hday, hmonth, hyear, calendarindex, direction):
		for row in range(0, 6):
			for column in range(0, 7):				
				newgday = int((self.refdate + timedelta(days=(calendarindex))).strftime("%d"))
				newgmonth = self.gmonths.index((self.refdate + timedelta(days=(calendarindex))).strftime("%B"))
				newgyear = int((self.refdate + timedelta(days=(calendarindex))).strftime("%Y"))
				newhyear, newhmonth, newhday = self.hijcal.goto_gregorian_day(newgyear, newgmonth+1, newgday)

				self.caltable.get_child_at(column,row).labelstack.get_child_by_name('Gregorian').day_next = newgday
				self.caltable.get_child_at(column,row).labelstack.get_child_by_name('Hijri').day_next = newhday
				
				if (column == 0) or (column == 6):
					self.caltable.get_child_at(column,row).labelstack.get_child_by_name('Gregorian').day_next_background = Color.LGrey
					self.caltable.get_child_at(column,row).labelstack.get_child_by_name('Hijri').day_next_background = Color.LGrey					
				else:
					self.caltable.get_child_at(column,row).labelstack.get_child_by_name('Gregorian').day_next_background = Color.White
					self.caltable.get_child_at(column,row).labelstack.get_child_by_name('Hijri').day_next_background = Color.White

				if newgmonth != self.gmonths.index(self.refdate.strftime("%B")):
					self.caltable.get_child_at(column,row).labelstack.get_child_by_name('Gregorian').day_next_background = Color.DGrey

				if newhmonth != hmonth:
					self.caltable.get_child_at(column,row).labelstack.get_child_by_name('Hijri').day_next_background = Color.DGrey

				if (newgday == self.gdtoday and newgmonth == self.gmtoday and newgyear == self.gytoday):
					self.caltable.get_child_at(column,row).labelstack.get_child_by_name('Gregorian').day_next_background = Color.Blue

				if (newhday == self.hdtoday and newhmonth == self.hmtoday and newhyear == self.hytoday):
					self.caltable.get_child_at(column,row).labelstack.get_child_by_name('Hijri').day_next_background = Color.Blue
				
				self.caltable.get_child_at(column,row).labelstack.get_child_by_name('Gregorian').set_transition_duration(300)
				self.caltable.get_child_at(column,row).labelstack.get_child_by_name('Hijri').set_transition_duration(300)

				if direction == Direction.LEFT:
					self.caltable.get_child_at(column,row).labelstack.get_child_by_name('Gregorian').set_visible_child_full('next', Gtk.StackTransitionType.SLIDE_LEFT)
					self.caltable.get_child_at(column,row).labelstack.get_child_by_name('Hijri').set_visible_child_full('next', Gtk.StackTransitionType.SLIDE_LEFT)
				else:
					self.caltable.get_child_at(column,row).labelstack.get_child_by_name('Gregorian').set_visible_child_full('next', Gtk.StackTransitionType.SLIDE_RIGHT)
					self.caltable.get_child_at(column,row).labelstack.get_child_by_name('Hijri').set_visible_child_full('next', Gtk.StackTransitionType.SLIDE_RIGHT)

				newgbackground = self.caltable.get_child_at(column,row).labelstack.get_child_by_name('Gregorian').day_next_background
				newhbackground = self.caltable.get_child_at(column,row).labelstack.get_child_by_name('Hijri').day_next_background

				self.caltable.get_child_at(column,row).labelstack.get_child_by_name('Gregorian').day = newgday
				self.caltable.get_child_at(column,row).labelstack.get_child_by_name('Gregorian').day_background = newgbackground
				self.caltable.get_child_at(column,row).labelstack.get_child_by_name('Hijri').day = newhday
				self.caltable.get_child_at(column,row).labelstack.get_child_by_name('Hijri').day_background = newhbackground

				if direction == Direction.LEFT:
					self.caltable.get_child_at(column,row).labelstack.get_child_by_name('Gregorian').set_visible_child_full('day', Gtk.StackTransitionType.SLIDE_LEFT)
					self.caltable.get_child_at(column,row).labelstack.get_child_by_name('Hijri').set_visible_child_full('day', Gtk.StackTransitionType.SLIDE_LEFT)
				else:
					self.caltable.get_child_at(column,row).labelstack.get_child_by_name('Gregorian').set_visible_child_full('day', Gtk.StackTransitionType.SLIDE_RIGHT)
					self.caltable.get_child_at(column,row).labelstack.get_child_by_name('Hijri').set_visible_child_full('day', Gtk.StackTransitionType.SLIDE_RIGHT)

				calendarindex += 1


class CalEntry(Gtk.EventBox):
	def __init__(self, gday, hday, gcolor, hcolor):
		Gtk.EventBox.__init__(self)
		self.set_events(Gdk.EventMask.BUTTON_PRESS_MASK)
		self.connect("button-press-event", self.on_day_pressed)

		self._state = State.Gregorian

		#Set up the stack for the labels
		self.labelstack = Gtk.Stack()
		self.labelstack.set_transition_type(Gtk.StackTransitionType.SLIDE_UP_DOWN)
		self.labelstack.set_transition_duration(300)

		#make the inactive label
		self.labelstack.add_named(CalEntryLabel(gday, gcolor), 'Gregorian')

		#make the active label
		self.labelstack.add_named(CalEntryLabel(hday, hcolor), 'Hijri')

		self.add(self.labelstack)
		self.show_all()

	@property
	def state(self):
		return self._state
		
	@state.setter
	def state(self, value):
		if value == State.Hijri:
			self.labelstack.set_visible_child_name('Hijri')
		else:
			self.labelstack.set_visible_child_name('Gregorian')
		self._state = value	

	def on_day_pressed(self, widget, data):	
		if self.state == State.Hijri:
			self.state = State.Gregorian
		else:
			self.state = State.Hijri


class CalEntryLabel(Gtk.Stack):
	def __init__(self, day, background):
		Gtk.Stack.__init__(self)

		self._day = day
		self._daynext = day
		self._daybackground = background
		self._daynextbackground = background

		#Box and label for the showing day
		self.labelboxday = Gtk.Box(halign=Gtk.Align.FILL, valign=Gtk.Align.FILL)
		self.labelday = Gtk.Label()
		self.labelday.set_use_markup(True)
		
		#Box and label for transitions
		self.labelboxnext = Gtk.Box(halign=Gtk.Align.FILL, valign=Gtk.Align.FILL)
		self.labelnext = Gtk.Label()
		self.labelnext.set_use_markup(True)

		#They are initialized the same
		self.day_background = background		
		self.day_next_background =background

		self.labelday.set_size_request(34,26)
		self.labelboxday.add(self.labelday)

		self.labelnext.set_size_request(34,26)
		self.labelboxnext.add(self.labelnext)

		##Add both to the stack
		self.add_named(self.labelboxday, 'day')
		self.add_named(self.labelboxnext, 'next')

	@property
	def day(self):
	    return self._day
	
	@day.setter
	def day(self, value):
	    self._day = value

	@property
	def day_next(self):
	    return self._daynext
	
	@day_next.setter
	def day_next(self, value):
	    self._daynext = value

	@property
	def day_background(self):
		return self._daybackground

	@day_background.setter
	def day_background(self, value):    
		if value == Color.White:
			self.labelboxday.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA.from_color(Gdk.Color.from_floats(1.0, 1.0, 1.0)))
			self.labelday.set_markup("<span>"+str(self.day)+"</span>")
		elif value == Color.Blue:
			self.labelboxday.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA.from_color(Gdk.Color.from_floats(0.316406, 0.671875, 0.996094)))
			self.labelday.set_markup("<span color=\"#ffffff\">"+str(self.day)+"</span>")
		elif value == Color.LGrey:
			self.labelboxday.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA.from_color(Gdk.Color.from_floats(0.917969, 0.917969, 0.917969)))
			self.labelday.set_markup("<span>"+str(self.day)+"</span>")
		elif value == Color.DGrey:
			self.labelboxday.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA.from_color(Gdk.Color.from_floats(0.839844, 0.839844, 0.839844)))
			self.labelday.set_markup("<span>"+str(self.day)+"</span>")
		self._daybackground = value
	
	@property
	def day_next_background(self):
		return self._daynextbackground

	@day_next_background.setter
	def day_next_background(self, value):
		if value == Color.White:
			self.labelboxnext.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA.from_color(Gdk.Color.from_floats(1.0, 1.0, 1.0)))
			self.labelnext.set_markup("<span>"+str(self.day_next)+"</span>")
		elif value == Color.Blue:
			self.labelboxnext.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA.from_color(Gdk.Color.from_floats(0.316406, 0.671875, 0.996094)))
			self.labelnext.set_markup("<span color=\"#ffffff\">"+str(self.day_next)+"</span>")
		elif value == Color.LGrey:
			self.labelboxnext.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA.from_color(Gdk.Color.from_floats(0.917969, 0.917969, 0.917969)))
			self.labelnext.set_markup("<span>"+str(self.day_next)+"</span>")
		elif value == Color.DGrey:
			self.labelboxnext.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA.from_color(Gdk.Color.from_floats(0.839844, 0.839844, 0.839844)))
			self.labelnext.set_markup("<span>"+str(self.day_next)+"</span>")
		self._daynextbackground = value


class Direction(object):
	LEFT, RIGHT = True, False

class State(object):
	Hijri, Gregorian = True, False

class Color(object):
	White, Blue, LGrey, DGrey = range(4)


GObject.type_register(CalEntry)
GObject.signal_new("sidebar-button-pressed", CalEntry, GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, ())