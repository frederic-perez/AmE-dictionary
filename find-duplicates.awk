BEGIN {
	for (i = 1; i < ARGC; ++i) {
		if (ARGV[i] == "-v")
			verbose = 1
		else if (ARGV[i] == "-d")
			debug = 1
		else if (ARGV[i] ~ /^-./) {
			e = sprintf("%s: unrecognized option -- %c", ARGV[0], substr(ARGV[i], 2, 1))
			print e > "/dev/stderr"
		} else
			break
		delete ARGV[i]
	}
	
	print "awk program called with the following options:"
	if (debug)
		print "  debug: on ('-d' in parameters)"
	else
		print "  debug: off"
	if (verbose)
		print "  verbose: on ('-v' in parameters)"
	else
		print "  verbose: off"

	FS = "__" # FS is the 'field separator'
	acc_fine_lines = 0
	acc_empty_lines = 0
	acc_weird_lines = 0
}

/^\r/ {
	++acc_empty_lines
	if (verbose)
		printf "empty line (L%d)\n", NR;
}

#/^[A-Za-záéíóú0-9 <>-&'\.()\/?,"!]+/ {
/^__[A-Za-záéíóú0-9 <>\-&'\.()\/?,"!]+__/ {
	++acc_fine_lines
	current_entry = $2
	if (current_entry in dictionary) {
		repeated[current_entry] = 1
	}
	if (verbose)
		printf "#%d: %s\n", acc_fine_lines, current_entry;
	dictionary[current_entry] = 1
}

#!/^[A-Za-záéíóú0-9 <>-&'\.()\/?,"!]+/ && !/^\r/ {
!/^__[A-Za-záéíóú0-9 <>\-&'\.()\/?,"!]+__/ && !/^\r/ {
	++acc_weird_lines
	#if (debug)
	printf "unmatched (and not empty) line (AKA weird line) at L%d: %s\n", NR, $0;
}

function length_of_array(a_array) {
	n = 0
	for (i in a_array)
		++n;
	return n
}

function check(a_array, a_array_name) {
	n = length_of_array(a_array)
	if (n > 0) {
		printf "Contents of '%s' (truncated to 10 elements), ", a_array_name, n; 
		n = 0;
		do_output_pseudo_sorting = 0
		if (do_output_pseudo_sorting) {
			print "pseudo-sorted ### WIP ###:"
			acc = 0
			while (acc < 10) {
				printf "  %s[%d] = %s\n", a_array_name, n, acc;
				++acc
			}
			printf "  %s[%d] = %s\n", a_array_name, n, i;
		} else {
			print "as it is:"
			for (i in a_array) {
				++n
				printf "  %s[%d] = %s\n", a_array_name, n, i;
				if (n == 10)
					break
			}
		}
	}
}

END {
	n = length_of_array(repeated)
	printf 	"Summary:\n  acc_fine_lines = %d\n  acc_empty_lines = %d\n  acc_weird_lines = %d\n  length('repeated') = %d\n",
		acc_fine_lines, acc_empty_lines, acc_weird_lines, n;
	check(repeated, "repeated")
}
