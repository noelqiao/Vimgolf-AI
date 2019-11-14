#! /usr/bin/env python3
# Copyright 2018 Tensorforce Team. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

from tensorforce.environments import Environment


class VimEnviron(Environment):
    """
    [MazeExplorer](https://github.com/mryellow/maze_explorer) environment adapter (specification
    key: `mazeexp`, `maze_explorer`).

    May require:
    ```bash
    sudo apt-get install freeglut3-dev

    pip3 install mazeexp
    ```

    Args:
        level (int): Game mode, see [GitHub](https://github.com/mryellow/maze_explorer)
            (<span style="color:#C00000"><b>required</b></span>).
        visualize (bool): Whether to visualize interaction
            (<span style="color:#00C000"><b>default</b></span>: false).


    WE NEED TO WRITE OUR OWN VIM ENVIRONMENT CLASS
    """

#    @classmethod
#    def levels(cls):
#        import mazeexp
#
#        return list(range(len(mazeexp.engine.config.modes)))

    def __init__(self, challenge, visualize=False, numSteps=None):
        import vimexp

        #assert level in MazeExplorer.levels()

        #self.environment = mazeexp.MazeExplorer(mode_id=level, visible=visualize)
        self.environment = vimexp.VimGolfer(challenge=challenge, visible=visualize)
        self.num_steps = numSteps

    def __str__(self):
        return super().__str__() + '({})'.format(self.environment.mode_id)

    def states(self):
       
        return self.environment.states

    def actions(self):
        print(dict(type='int', num_actions=self.environment.actions_num))
        return dict(type='int', num_actions=self.environment.actions_num)

    def close(self):
        self.environment.reset()
        self.environment = None

    def reset(self):
        return self.environment.reset()

    def execute(self, actions):
        state, reward, terminal, _ = self.environment.act(action=actions)
        return state, terminal, reward
    def max_episode_timesteps(self):
        return self.num_steps


if __name__ == '__main__':
    vim_environ = VimEnviron('OneNumberPerLine')
    vim_environ.actions()
