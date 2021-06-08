#!/usr/bin/env python

from tyrell.enumerator.bidirection_smt import BidirectEnumerator
import tyrell.spec as S
from tyrell.interpreter import PostOrderInterpreter
from tyrell.enumerator import SmtEnumerator, RelaxedRandomEnumerator
from tyrell.decider import Example, ExampleConstraintDecider
from tyrell.synthesizer import Synthesizer
from tyrell.logger import get_logger

logger = get_logger('tyrell')


class ToyInterpreter(PostOrderInterpreter):

    def eval_make_header(self, node, args):
        return "# " + args[0]

    def eval_make_header2(self, node, args):
        return "## " + args[0]

    def eval_make_header3(self, node, args):
        return "### " + args[0]

    def eval_paragraph(self, node, args):
        return args[0]

    def eval_newline(self, node, args):
        return args[0] + "\n" + args[1]

    def eval_bold(self, node, args):
        return "**" + args[0] + "**"

    def eval_italic(self, node, args):
        return "*" + args[0] + "*"


def main():

    logger.info('Parsing Spec...')
    spec = S.parse_file('example/markdown.tyrell')
    logger.info('Parsing succeeded')

    sketches = [line.strip() for line in open("./static/demo-mkdwn-size3.txt", 'r')]

    logger.info('Building synthesizer...')
    synthesizer = Synthesizer(
        # enumerator=SmtEnumerator(spec, depth=3, loc=1), # plus(@param1, @param0) / plus(@param0, @param1)
        enumerator=BidirectEnumerator(spec, depth=1, loc=1, sk_queue=sketches), # plus(plus(@param0, const(_apple_)), @param1)
        decider=ExampleConstraintDecider(
            spec=spec,
            interpreter=ToyInterpreter(),
            examples=[
                Example(input=["Lorem Ipsum"], output="# Lorem Ipsum"), # depth 1
                Example(input=["Lorem Ipsum Dolor, different header phrase!"], output="# Lorem Ipsum Dolor, different header phrase!"), # depth 1
                # Example(input=["Lorum Ipsum", "Some Text"], output="### Lorum Ipsum\nSome Text"), # depth 2
                # Example(input=["Lorum Ipsum", "Some Text"], output="# *Lorum Ipsum*\nSome Text"), # depth 3
                # Example(input=["Lorum Ipsum", "Some Text"], output="## **Lorum Ipsum**\n*Some Text*"), # depth 3
            ],
        )
    )
    logger.info('Synthesizing programs...')

    prog = synthesizer.synthesize()
    if prog is not None:
        logger.info('Solution found: {}'.format(prog))
    else:
        logger.info('Solution not found!')


if __name__ == '__main__':
    logger.setLevel('DEBUG')
    main()
