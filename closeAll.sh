#!/bin/bash
prefix="captcha_cracker"
k="ps aux | grep "$prefix" | awk '{print \$2}' | xargs kill"
kc="ps aux | grep Chrome | awk '{print \$2}' | xargs kill"
eval ${k}
eval ${kc}

