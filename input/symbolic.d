fun symbolic(a,b,c) = {
    int x = 0;
    int y = 0;
    int z = 0;

    if a then
        x = -2;
    endif;
    
    if b > 5 then
        if !a & c then
			y = 1;
		endif;
		z = 2;
    endif;

    if x + y + z != 3 then
        printf "PASS";
    endif;
}