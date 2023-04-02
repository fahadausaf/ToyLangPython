function symbolic(a,b,c) = {
    int x = 1;
    int y = 2;
    int z = 3 + x;

    if a then
        x = -2;
    endif;
    
    if b > 5 then
        if !a & c then
			y = 1;
        else
            y = 78;
		endif;
		z = 2;
    endif;

    if x + y + z != 3 then
        printf "PASS";
    endif;
}