#!/bin/sh
# based on script by (c) vip at linux.pl, wolf at pld-linux.org

MOZILLA_FIVE_HOME=/usr/lib/mozilla-thunderbird
if [ "$1" == "-remote" ]; then
	/usr/lib/mozilla-thunderbird/thunderbird "$@"
else
	PING=`/usr/lib/mozilla-thunderbird/thunderbird -remote 'ping()' 2>&1 >/dev/null`
	if [ -n "$PING" ]; then
		/usr/lib/mozilla-thunderbird/thunderbird "$@"
	else
		case "$1" in
		    -compose|-editor)
			/usr/lib/mozilla-thunderbird/thunderbird -remote 'xfeDoCommand (composeMessage)'
			;;
		    *)
			/usr/lib/mozilla-thunderbird/thunderbird -remote 'xfeDoCommand (openInbox)'
			;;
		esac
	fi
fi
