#!/bin/sh
# based on script by (c) vip at linux.pl, wolf at pld-linux.org

MOZILLA_FIVE_HOME="@LIBDIR@/mozilla-thunderbird"

MOZARGS=
MOZLOCALE="$(/usr/bin/locale | grep "^LC_MESSAGES=" | \
		sed -e "s|LC_MESSAGES=||g" -e "s|\"||g" )"
for MOZLANG in $(echo $LANGUAGE | tr ":" " ") $MOZLOCALE; do
	eval MOZLANG="$(echo $MOZLANG | sed -e "s|_\([^.]*\).*|-\1|g")"

	if [ -f $MOZILLA_FIVE_HOME/chrome/$MOZLANG.jar ]; then
		MOZARGS="-UILocale $MOZLANG"
		break
	fi
done

if [ -z "$MOZARGS" ]; then
	# try harder
	for MOZLANG in $(echo $LANGUAGE | tr ":" " ") $MOZLOCALE; do
		eval MOZLANG="$(echo $MOZLANG | sed -e "s|_.*||g")"

		LANGFILE=$(echo ${MOZILLA_FIVE_HOME}/chrome/${MOZLANG}*.jar \
				| sed 's/\s.*//g' )
		if [ -f "$LANGFILE" ]; then
			MOZLANG=$(basename "$LANGFILE" | sed 's/\.jar//')
			MOZARGS="-UILocale $MOZLANG"
			break
		fi
	done
fi

if [ -n "$MOZARGS" ]; then
	THUNDERBIRD="$MOZILLA_FIVE_HOME/thunderbird $MOZARGS"
else
	THUNDERBIRD="$MOZILLA_FIVE_HOME/thunderbird"
fi

if [ "$1" == "-remote" ]; then
	$THUNDERBIRD "$@"
else
	PING=`$THUNDERBIRD -remote 'ping()' 2>&1 >/dev/null`
	if [ -n "$PING" ]; then
		$THUNDERBIRD "$@"
	else
		case "$1" in
		    -compose|-editor)
			$THUNDERBIRD -remote 'xfeDoCommand (composeMessage)'
			;;
		    *)
			$THUNDERBIRD -remote 'xfeDoCommand (openInbox)'
			;;
		esac
	fi
fi
