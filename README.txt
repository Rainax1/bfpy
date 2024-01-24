This is just a Brainfuck interpreter written in Python.

Usage:
 ./brainfuck.py 
    this will launch script in live interpreter mode, there is and example of hello world 

    bf [1] # ++++++++++[>+++++++>++++++++++>+++>+<<<<-]>++.>+.+++++++..+++.>++.<<+++++++++++++++.>.+++.------.--------.>+.>.

    or

    bf [1] # help
    


 ./brainfuck.py com yourcode.bf

You can use it as a module as well:

  import brainfuck

  sourcecode = """
    ++++++++++[>+++++++>++++++++++>+++>+<<<<-]
    >++.>+.+++++++..+++.>++.<<+++++++++++++++.
    >.+++.------.--------.>+.>.
  """

  brainfuck.evaluate(sourcecode)

http://en.wikipedia.org/wiki/Brainfuck

This programm is licensed under the terms of the
DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE.
