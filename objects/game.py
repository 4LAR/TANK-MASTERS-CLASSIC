def play():
    clear_display()
    add_display(world())
    for i in range(4):
        add_display(player(i))
