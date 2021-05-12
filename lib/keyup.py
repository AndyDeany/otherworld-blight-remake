keys = pygame.key.get_pressed()
# Miscellaneous
if backspace_held and not keys[8]:
    backspace = 1
    backspace_held = 0
    backspace_held_time = 0
    backspace_allowed = 1
if tab_held and not keys[9]:
    tab = 1
    tab_held = 0
    tab_held_time = 0
    tab_allowed = 1
if enter_held and not keys[13]:
    enter = 1
    enter_held = 0
    enter_held_time = 0
    enter_allowed = 1
if pausebreak_held and not keys[19]:
    pausebreak = 1
    pausebreak_held = 0
    pausebreak_held_time = 0
    pausebreak_allowed = 1
if escape_held and not keys[27]:
    escape = 1
    escape_held = 0
    escape_held_time = 0
    escape_allowed = 1
if space_held and not keys[32]:            
    space = 1
    space_held = 0
    space_held_time = 0
    space_allowed = 1
if apostrophe_held and not keys[39]:
    apostrophe = 1
    apostrophe_held = 0
    apostrophe_held_time = 0
    apostrophe_allowed = 1
if comma_held and not keys[44]:
    comma = 1
    comma_held = 0
    comma_held_time = 0
    comma_allowed = 1
if minus_held and not keys[45]:
    minus = 1
    minus_held = 0
    minus_held_time = 0
    minus_allowed = 1
if fullstop_held and not keys[46]:
    fullstop = 1
    fullstop_held = 0
    fullstop_held_time = 0
    fullstop_allowed = 1
if forwardslash_held and not keys[47]:               
    forwardslash = 1
    forwardslash_held = 0
    forwardslash_held_time = 0
    forwardslash_allowed = 1
# Numbers across the top
if zero_held and not keys[48]:
    zero = 1
    zero_held = 0
    zero_held_time = 0
    zero_allowed = 1
if one_held and not keys[49]:
    one = 1
    one_held = 0
    one_held_time = 0
    one_allowed = 1
if two_held and not keys[50]:
    two = 1
    two_held = 0
    two_held_time = 0
    two_allowed = 1
if three_held and not keys[51]:
    three = 1
    three_held = 0
    three_held_time = 0
    three_allowed = 1
if four_held and not keys[52]:
    four = 1
    four_held = 0
    four_held_time = 0
    four_allowed = 1
if five_held and not keys[53]:
    five = 1
    five_held = 0
    five_held_time = 0
    five_allowed = 1
if six_held and not keys[54]:
    six = 1
    six_held = 0
    six_held_time = 0
    six_allowed = 1
if seven_held and not keys[55]:
    seven = 1
    seven_held = 0
    seven_held_time = 0
    seven_allowed = 1
if eight_held and not keys[56]:
    eight = 1
    eight_held = 0
    eight_held_time = 0
    eight_allowed = 1
if nine_held and not keys[57]:
    nine = 1
    nine_held = 0
    nine_held_time = 0
    nine_allowed = 1
# Miscellaneous
if semicolon_held and not keys[59]:
    semicolon = 1
    semicolon_held = 0
    semicolon_held_time = 0
    semicolon_allowed = 1
if backslash_held and not keys[60]:
    backslash = 1
    backslash_held = 0
    backslash_held_time = 0
    backslash_allowed = 1
if equals_held and not keys[61]:
    equals = 1
    equals_held = 0
    equals_held_time = 0
    equals_allowed = 1
if opensquarebracket_held and not keys[91]:
    opensquarebracket = 1
    opensquarebracket_held = 0
    opensquarebracket_held_time = 0
    opensquarebracket_allowed = 1
if sharp_held and not keys[92]:
    sharp = 1
    sharp_held = 0
    sharp_held_time = 0
    sharp_allowed = 1
if closesquarebracket_held and not keys[93]:
    closesquarebracket = 1
    closesquarebracket_held = 0
    closesquarebracket_held_time = 0
    closesquarebracket_allowed = 1
if backtick_held and not keys[96]:
    backtick = 1
    backtick_held = 0
    backtick_held_time = 0
    backtick_allowed = 1
# Alphabet
if a_held and not keys[97]:
    a = 1
    a_held = 0
    a_held_time = 0
    a_allowed = 1
if b_held and not keys[98]:
    b = 1
    b_held = 0
    b_held_time = 0
    b_allowed = 1
if c_held and not keys[99]:
    c = 1
    c_held = 0
    c_held_time = 0
    c_allowed = 1
if d_held and not keys[100]:
    d = 1
    d_held = 0
    d_held_time = 0
    d_allowed = 1
if e_held and not keys[101]:
    e = 1
    e_held = 0
    e_held_time = 0
    e_allowed = 1
if f_held and not keys[102]:
    f = 1
    f_held = 0
    f_held_time = 0
    f_allowed = 1
if g_held and not keys[103]:
    g = 1
    g_held = 0
    g_held_time = 0
    g_allowed = 1
if h_held and not keys[104]:
    h = 1
    h_held = 0
    h_held_time = 0
    h_allowed = 1
if i_held and not keys[105]:
    i = 1
    i_held = 0
    i_held_time = 0
    i_allowed = 1
if j_held and not keys[106]:
    j = 1
    j_held = 0
    j_held_time = 0
    j_allowed = 1
if k_held and not keys[107]:
    k = 1
    k_held = 0
    k_held_time = 0
    k_allowed = 1
if l_held and not keys[108]:
    l = 1
    l_held = 0
    l_held_time = 0
    l_allowed = 1
if m_held and not keys[109]:
    m = 1
    m_held = 0
    m_held_time = 0
    m_allowed = 1
if n_held and not keys[110]:
    n = 1
    n_held = 0
    n_held_time = 0
    n_allowed = 1
if o_held and not keys[111]:
    o = 1
    o_held = 0
    o_held_time = 0
    o_allowed = 1
if p_held and not keys[112]:
    p = 1
    p_held = 0
    p_held_time = 0
    p_allowed = 1
if q_held and not keys[113]:
    q = 1
    q_held = 0
    q_held_time = 0
    q_allowed = 1
if r_held and not keys[114]:
    r = 1
    r_held = 0
    r_held_time = 0
    r_allowed = 1
if s_held and not keys[115]:
    s = 1
    s_held = 0
    s_held_time = 0
    s_allowed = 1
if t_held and not keys[116]:
    t = 1
    t_held = 0
    t_held_time = 0
    t_allowed = 1
if u_held and not keys[117]:
    u = 1
    u_held = 0
    u_held_time = 0
    u_allowed = 1
if v_held and not keys[118]:
    v = 1
    v_held = 0
    v_held_time = 0
    v_allowed = 1
if w_held and not keys[119]:
    w = 1
    w_held = 0
    w_held_time = 0
    w_allowed = 1
if x_held and not keys[120]:
    x = 1
    x_held = 0
    x_held_time = 0
    x_allowed = 1
if y_held and not keys[121]:
    y = 1
    y_held = 0
    y_held_time = 0
    y_allowed = 1
if z_held and not keys[122]:
    z = 1
    z_held = 0
    z_held_time = 0
    z_allowed = 1
# Miscellaneous
if delete_held and not keys[127]:
    delete = 1
    delete_held = 0
    delete_held_time = 0
    delete_allowed = 1
# Numpad
if numpad0_held and not keys[256]:
    numpad0 = 1
    numpad0_held = 0
    numpad0_held_time = 0
    numpad0_allowed = 1
if numpad1_held and not keys[257]:
    numpad1 = 1
    numpad1_held = 0
    numpad1_held_time = 0
    numpad1_allowed = 1
if numpad2_held and not keys[258]:
    numpad2 = 1
    numpad2_held = 0
    numpad2_held_time = 0
    numpad2_allowed = 1
if numpad3_held and not keys[259]:
    numpad3 = 1
    numpad3_held = 0
    numpad3_held_time = 0
    numpad3_allowed = 1
if numpad4_held and not keys[260]:
    numpad4 = 1
    numpad4_held = 0
    numpad4_held_time = 0
    numpad4_allowed = 1
if numpad5_held and not keys[261]:
    numpad5 = 1
    numpad5_held = 0
    numpad5_held_time = 0
    numpad5_allowed = 1
if numpad6_held and not keys[262]:
    numpad6 = 1
    numpad6_held = 0
    numpad6_held_time = 0
    numpad6_allowed = 1
if numpad7_held and not keys[263]:
    numpad7 = 1
    numpad7_held = 0
    numpad7_held_time = 0
    numpad7_allowed = 1
if numpad8_held and not keys[264]:
    numpad8 = 1
    numpad8_held = 0
    numpad8_held_time = 0
    numpad8_allowed = 1
if numpad9_held and not keys[265]:
    numpad9 = 1
    numpad9_held = 0
    numpad9_held_time = 0
    numpad9_allowed = 1
if numpaddivide_held and not keys[267]:
    numpaddivide = 1
    numpaddivide_held = 0
    numpaddivide_held_time = 0
    numpaddivide_allowed = 1
if numpadmultiply_held and not keys[268]:
    numpadmultiply = 1
    numpadmultiply_held = 0
    numpadmultiply_held_time = 0
    numpadmultiply_allowed = 1
if numpadminus_held and not keys[269]:
    numpadminus = 1
    numpadminus_held = 0
    numpadminus_held_time = 0
    numpadminus_allowed = 1
if numpadplus_held and not keys[270]:         
    numpadplus = 1
    numpadplus_held = 0
    numpadplus_held_time = 0
    numpadplus_allowed = 1
if numpadenter_held and not keys[271]:
    numpadenter = 1
    numpadenter_held = 0
    numpadenter_held_time = 0
    numpadenter_allowed = 1
# Arrow keys
if uparrow_held and not keys[273]:
    uparrow = 1
    uparrow_held = 0
    uparrow_held_time = 0
    uparrow_allowed = 1
if downarrow_held and not keys[274]:
    downarrow = 1
    downarrow_held = 0
    downarrow_held_time = 0
    downarrow_allowed = 1
if rightarrow_held and not keys[275]:
    rightarrow = 1
    rightarrow_held = 0
    rightarrow_held_time = 0
    rightarrow_allowed = 1
if leftarrow_held and not keys[276]:
    leftarrow = 1
    leftarrow_held = 0
    leftarrow_held_time = 0
    leftarrow_allowed = 1
# Miscellaneous
if insert_held and not keys[277]:
    insert = 1
    insert_held = 0
if home_held and not keys[278]:
    home = 1
    home_held = 0
if end_held and not keys[279]:
    end = 1
    end_held = 0
if pageup_held and not keys[280]:
    pageup = 1
    pageup_held = 0
if pagedown_held and not keys[281]:
    pagedown = 1
    pagedown_held = 0
# F keys
if f1_held and not keys[282]:
    f1 = 1
    f1_held = 0
if f2_held and not keys[283]:
    f2 = 1
    f2_held = 0
if f3_held and not keys[284]:
    f3 = 1
    f3_held = 0
if f4_held and not keys[285]:
    f4 = 1
    f4_held = 0    
if f5_held and not keys[286]:
    f5 = 1
    f5_held = 0
if f6_held and not keys[287]:
    f6 = 1
    f6_held = 0
if f7_held and not keys[288]:
    f7 = 1
    f7_held = 0
if f8_held and not keys[289]:
    f8 = 1
    f8_held = 0
if f9_held and not keys[290]:
    f9 = 1
    f9_held = 0
if f10_held and not keys[291]:
    f10 = 1
    f10_held = 0
if f11_held and not keys[292]:
    f11 = 1
    f11_held = 0
if f12_held and not keys[293]:
    f12 = 1
    f12_held = 0
# Key modifiers
if numlock and not keys[300]:
    numlock = 1
    numlock = 0
if capslock and not keys[301]:
    capslock = 1
    capslock = 0
if scrolllock_held and not keys[302]:
    scrolllock = 1
    scrolllock_held = 0
if rightshift_held and not keys[303]:
    rightshift = 1
    rightshift_held = 0
if leftshift_held and not keys[304]:
    leftshift = 1
    leftshift_held = 0
if rightshift or leftshift:
    shift = 1
    shift_held = 0
if rightcontrol_held and not keys[305]:
    rightcontrol = 1
    rightcontrol_held = 0
if leftcontrol_held and not keys[306]:
    leftcontrol = 1
    leftcontrol_held = 0
if altgrammar_held and not keys[307]:
    altgrammar = 1
    altgrammar_held = 0
if alt_held and not keys[308]:
    alt = 1
    alt_held = 0
if leftwindows_held and not keys[311]:    #} these might be
    leftwindows = 1
    leftwindows_held = 0
if rightwindows_held and not keys[312]:   #} pointless (windows keys)
    rightwindows = 1
    rightwindows_held = 0
if menubutton_held and not keys[319]:
    menubutton = 1
    menubutton_held = 0
