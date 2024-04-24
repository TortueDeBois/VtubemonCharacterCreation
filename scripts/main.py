from js import File, Uint8Array, window, navigator
import js
from io import BytesIO
import random
import json
import sys
import os
from pathlib import Path
from pyodide.http import pyfetch
import asyncio
from PIL import Image
from PIL.PngImagePlugin import PngInfo

Body_32x32_01 = 'iVBORw0KGgoAAAANSUhEUgAAAI4AAABMCAYAAAC73Y+3AAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAyZpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDkuMS1jMDAyIDc5LmYzNTRlZmM3MCwgMjAyMy8xMS8wOS0xMjowNTo1MyAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RSZWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZVJlZiMiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIDI1LjQgKFdpbmRvd3MpIiB4bXBNTTpJbnN0YW5jZUlEPSJ4bXAuaWlkOjdGRDI3NjFGQkZCNDExRUVBM0E5RjRCRDEwMURERUMxIiB4bXBNTTpEb2N1bWVudElEPSJ4bXAuZGlkOjdGRDI3NjIwQkZCNDExRUVBM0E5RjRCRDEwMURERUMxIj4gPHhtcE1NOkRlcml2ZWRGcm9tIHN0UmVmOmluc3RhbmNlSUQ9InhtcC5paWQ6N0ZEMjc2MURCRkI0MTFFRUEzQTlGNEJEMTAxRERFQzEiIHN0UmVmOmRvY3VtZW50SUQ9InhtcC5kaWQ6N0ZEMjc2MUVCRkI0MTFFRUEzQTlGNEJEMTAxRERFQzEiLz4gPC9yZGY6RGVzY3JpcHRpb24+IDwvcmRmOlJERj4gPC94OnhtcG1ldGE+IDw/eHBhY2tldCBlbmQ9InIiPz54nvu/AAAFgUlEQVR42uydz28TRxTHd4PjxE5oSjAqJAVEaVVAICFx41B6KVxBQuIGf0K5IqQeKkWc+RPojRO9Qi9w4RapEghSFYEIDSICQgn5hWNsVrP7Tb2PGe/senZtmu/nsnFiz3tvePOdtzOzxm+1Wh4haRlgFxAmDmHiECYOYeIQwsQhTBzCxCFMHMLEIYSJQ5g4hIlDmDiEiUMIE4cwcQgThzBxyGahhB9831fXkyfPq+uBr4bVdWZ+LdOh5EO7t6oGHzx7p17fuvWb1edc2QdBO37UTiY/gji8KI5WEfaLjj/rmXMqDsmEj4w7deqCNtMv/TSh/eDg+NaODf96/a9UI8400mDfZG994V1HP6788dyJH7+c+76jHZMftvZ7FT8Vh/SmxgFJSmPKdDki8Pkg45HSvo1Drkaaaz+Kst8v8VNxSL6KMzk6qK5zS+uZGkoaAXu2lWNzOeZYvMbfZ9/UuxphSWT1w5V99DPsSb+Kjp+KQ3qjOIHSqDnw52M1pwaS5th6/X000jxtTeFqpEk/ArvauT4Y8VY1XlrQr1enX2nt90v8VBxSjOIsLS1GP9UKdaDZ/CDsT+RqD3ZKpVJPOtxk/3OLn4pD3KzjFE2j0dhUdv8v9qk4hIlDmDjkc61xVhbCFczqeDlfB6LqHnNuXnbRrrSbN9KuyX7RNQ/vqkhvFWd09IvezJUDWyL7VauR2i2IEyvWRSPtDwyEY3d4uFqI4sJ+o7He3b8bxw7pSnF2VsJDx9hLkXtWaUfC5Rsz6jp15oCYy+OZXi4Pqet328od7XdL0G7Mzt9vPK1fpdKgVRxpa0PYRz+/8Ia0nzf1r60fpvfJdmWcVBxSrOLMvl0Tc39NW2tknYOxRwKFATgPU//xnLoe2VFRI3LqzmOlPJdPfNNVgEE76nps8kvV7r35cLf59u3rsfc1m82Yn2n3jEz9JOOfrQ/F7LedA1L+YfcaitttrQM/oHiwYzr3Q8UhxSgOlObgjpGOI940ApDZy3P/qOvFb8uxOffwZPic1f25+PmS48dPq+v+sdCV6bl/Y3ahGFlpa0e1e2RXqDxlcQIQ8cPPwO9Wexwv74V+jEx+re0HvJZKA//Rrw9fLmuVqF4Z0/oPu/Aj6W7T5C/4sO7m/+6g4pBMbDxXhSc5oQB7xoZR+1ilqGkdaLu3qhp+Gp1lvnv3d63iBDipaWzvrrzoJKJ8vgn+7I3OBr/2Kq1ONVsSQT/67TWkbfxtfjqh7QRiLP6bN69RcUgPahywMSL+GwmeruaQyoBMRmbjfWvRnohppO2rhSumT16tpFrXyHq3s6EEhqcd4Gfph7PR+s6ip1MCGb/sF7w2KQ3s7hwJBe1RdLeHeF2vY8l+RPyscUhvFSdrBpt+n7TrGyiNGnJypTPtim3SOg7asX2yUfptuovqlhfLvjb+vE4luHqyk4pDilGcvHfR89oVz/t8kat+gZ9SKbMC5Ubt5Sp+Kg4ptsZxNYLlSm1eyBXoo3vHld1HrxtOFCIr+N4a1By260NZ44cywi4Vh/SX4mDlE3s94Op0/H1Yd8Ccuq9W9aO7Jm27mvUiOQJcK1Cs/T+fLmjXVySIA4qIWgHfdAWgFFN3FmP9hnUcycaKdbSeg2e5cSKw2Ww6jT9o14/sqNcz86xxSD8pjmkF2bbKh9IkjegOezda5Eg3rVPY2ksbP2q6T+1MxBTXtGJsVJ6c48d5I3kOyfO4V0X6+a7KdBeBqt107sbVXQtqiUqlGqtZVlfDFeiVhXy+bUPe/eW9i99v8VNxSLGKI08Gmv4OpbGtJdLaM52kS/t+W2StY9sPWe31W/xUHOJ2bSPrN2uTzQ0VhzBxCBOHMHEIE4cQJg5h4hAmDmHiECYOIUwc4oCPAgwA9SssLiSuO8UAAAAASUVORK5CYII='
Body_32x32_02 = 'iVBORw0KGgoAAAANSUhEUgAAAI4AAABMCAYAAAC73Y+3AAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAyZpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDkuMS1jMDAyIDc5LmYzNTRlZmM3MCwgMjAyMy8xMS8wOS0xMjowNTo1MyAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RSZWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZVJlZiMiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIDI1LjQgKFdpbmRvd3MpIiB4bXBNTTpJbnN0YW5jZUlEPSJ4bXAuaWlkOjg1QUU0NTRBQkZCNDExRUVCMEVBOEJCNENCMEJBOTcxIiB4bXBNTTpEb2N1bWVudElEPSJ4bXAuZGlkOjg1QUU0NTRCQkZCNDExRUVCMEVBOEJCNENCMEJBOTcxIj4gPHhtcE1NOkRlcml2ZWRGcm9tIHN0UmVmOmluc3RhbmNlSUQ9InhtcC5paWQ6ODVBRTQ1NDhCRkI0MTFFRUIwRUE4QkI0Q0IwQkE5NzEiIHN0UmVmOmRvY3VtZW50SUQ9InhtcC5kaWQ6ODVBRTQ1NDlCRkI0MTFFRUIwRUE4QkI0Q0IwQkE5NzEiLz4gPC9yZGY6RGVzY3JpcHRpb24+IDwvcmRmOlJERj4gPC94OnhtcG1ldGE+IDw/eHBhY2tldCBlbmQ9InIiPz7IZIxbAAAFvklEQVR42uxcz28bRRT2Olv/SE1aKKItKgIFIVQhyoVTDhWnVuoBcUDiBn8DB25FVRVuPeRvoBISSBwQh0rtKerBJy5EQm2FiqioaKAF0sitE3uzyzIzX+wZ79jr3dm1S77vMtl4Pe+90XvfvHkzYy+KogpBTIsqh4Cg4xB0HIKOQ9BxCIKOQ9BxCDoOQcch6DgEQcch6DgEHYeg4xB0HIKg4xB0HIKOQ9BxiIMCH394nifac+c+Fu2bL8qzyHceeZkOJZ9+uSo6vPV7KJ5v3Lia6nuu5ANxP57qJ5MesR0VZUdUhvyy7c965pyMQ2SCB487f/6TRE//7GyY+MX60ebYjr/4fneqiLNFGuTb5O1udcfqceVm1YkeF9+vj5Vj0yOt/FnZT8YhZpPjAJOYxubpZkTg+7HHw6W9NAq5ijTXepQlf17sJ+MQxTLOqcN7or3/ZCFTR5Mi4JUjkTaXY47FMz7/7bGXK8ImIaseruRjnCHP1Kts+8k4xGwYJ2Ya4YqfnoFn150ImDTH9nq7KtLqiTmFq0gz9YjlJoZ2HPGpcrxpgXFd22gmyp8X+8k4RDmM0+lsq78OlapAGO4Z8luFyoMc3/dnMuA2+c+a/WQcwk0dp2wEQXCg5P5f5JNxCDoOQcchntUcJ9iS9RX/aL1YBVR2jzm3KLno15RbeC5hyLXJLzvn4aqKmC3jtFpL6q9uqQpUqwtK/qIm3xapeQE7UbEuG6b8alXGbqOxqOzuFsq4kB8EfTIOMUPGOdnoib0L7KUM9qyy5TyXrnVEe/lCy5jLdU+v1WR/bxzZGys/L+J+NTk/P64n6uX7h1LZMW1uCPkY5weWvUDb+KbVw/ae2a9pJxmHKJdx7m1Hau7V96zMXCPrqgd7JGAYAOdheu99JNozx+Su7Wo7EAp9vpIvMlbbkknePSnP3G48lDnV+vpX2nthGGp6TrtnZBsn0/57vbqSP3IOSOiH3Wswbt5cB3qA8SDHdu6HjEOUwzjI8k8f81TE9xMj3hYB8Oxo8x/RXlzGnCvbt074ot+fNvVIXFn5QLSvP9cT7Q8PIk0uGCMrhvoR/b59XN73qhknAGE/9IxzBXm7YVnmDP3bsvVOPJ+cM6hnk2mgP8b11l/JTBQ0Gsj6tM/7tze18Qy2xjOwTV8gCnDeZ4GMQ5SP/XtVuMkJBnh1yUPuk+rizaAOpOOlaFt09MsT+dxuf5fIOP8Fg4ucJu3qqqJOIpr3m6DP8mH5/Ke3FI3L2SYhHkdvOIdMa/+Qnk4wdAJRs//69S/JOMQMchxgPyIGkVBJyjlMZljb0D0b7+2oPZF2+9vESHvtBTnX/vr33lR1jayrHcB22wH2+2c/VPWd7UoSE5j2m+OCZxvTQO7x5o5o7z7safa6rmOZ4wj7meMQs2WcrB48+v++itjxu74x0wjXR6UTDIGIvXwhH+OYTJD2ZqOpt20VNbT+yaTfH92Gsr/mlGltcHWzk4xDlMM4g9VTyNFLHJd8ucko4+a79YC9KzCuKyYj4xDl5jiuTuqZldqiMKhAy/adUw0h9+5WzdGqLVvdBb9bg5yj0+kXan+r1dTkknGI+WIcVD6x14OIXdvQK8WoO1y61kd9xhtXn0moF5kR4JqBtP5/vL+j9Ph67JdgBxgRucKVm02NaVBJXm3r44Y6jon9irWq5+AuN04EhmHo1P64X0/JEc93HuWbKcg4hFvGsVWQB1m+uarS6zdgGrNiapWjsGLIM4HftJtUp0grb1r7kdONymlpqxhbxdjKPAXbj/NG6+vfGJ9wr4qY51WVbe8HWfvg3I2be0KjJ+mknGZzUctZut2nkXy/mN11c/VX9C7+vNlPxiHKZRzzZKDtczBN2lxiWnmDk3RPp3w/2yLFzHXSjkNWefNmPxmHcFvbyPrL2sTBBhmHoOMQdByCjkPQcQiCjkPQcQg6DkHHIeg4BEHHIRzgXwEGAESvPbpNpfFEAAAAAElFTkSuQmCC'
Hair_01 = 'iVBORw0KGgoAAAANSUhEUgAAAI4AAABMCAYAAAC73Y+3AAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAyZpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDkuMS1jMDAyIDc5LmYzNTRlZmM3MCwgMjAyMy8xMS8wOS0xMjowNTo1MyAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RSZWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZVJlZiMiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIDI1LjQgKFdpbmRvd3MpIiB4bXBNTTpJbnN0YW5jZUlEPSJ4bXAuaWlkOjhCRkNBOTg4QkZCNDExRUU4MDJCRDUxRDdFRTYxMjAyIiB4bXBNTTpEb2N1bWVudElEPSJ4bXAuZGlkOjhCRkNBOTg5QkZCNDExRUU4MDJCRDUxRDdFRTYxMjAyIj4gPHhtcE1NOkRlcml2ZWRGcm9tIHN0UmVmOmluc3RhbmNlSUQ9InhtcC5paWQ6OEJGQ0E5ODZCRkI0MTFFRTgwMkJENTFEN0VFNjEyMDIiIHN0UmVmOmRvY3VtZW50SUQ9InhtcC5kaWQ6OEJGQ0E5ODdCRkI0MTFFRTgwMkJENTFEN0VFNjEyMDIiLz4gPC9yZGY6RGVzY3JpcHRpb24+IDwvcmRmOlJERj4gPC94OnhtcG1ldGE+IDw/eHBhY2tldCBlbmQ9InIiPz6tED9kAAAEWUlEQVR42uydzWsUSRiHq5OxJzGTbC5iorAaI4KwCrK34G0hQVDw4EFYWI8e/Vv2uMcVBAUPgoIkKOSweFoxrF5cP6KCRslBVxOcGWcy21b1G+1K93R198w46vNcajo9VW9V5Ve/evsjxGu1WgogKwNMASAcQDiAcADhACAcQDiAcADhAMIBQDiAcADhAMIBhAOAcADhAMIBhAPfCyX54HmeLmdnf9PlyEBNl+sb5VwvJQf1vbC+Pl5YOO9Ur1Px+6UfWeP3avxF3zXHcSAXnihvbu5MrNKnyquRCkPl9g1WTXW1XNuRacUlrTSJ7xrXJm8/RkumwXcNt34UjS9xy+q9LmtquFBcO37Qrhe2q4/n5//EceAL5jhCktO4IitjSq2K4mUz9VzqZ3UaO669AqWdrP0Qpzk41n4efr98fc/H8uyJY0/jzmeNL06zQz0Px+VnGvcfV6P9kXZW1e5M48dxoLs5zvG507r8oNwcJ2uuM+TVtdKrLT+yx8veHpxX4flCuVXaXp+3H3Z8cRqbJOeR+NuUyXWCeY6cD37edv7TchxxmqT+2PGvzV/EceAL5jiidNkTlfILrXDXPb5eDxvy2zudazzXfgRxY/f6JMeT+LLyz50yKzktxxHsXGNLfL/9/KeNX+LbOU5S/KK5Do4DxRxnbe2tUWYlPK6Zvb6SktUXZWOjGYmvyt0dsMQplUq56tsrP81pZB7T4tvzn5fU/sg8c1UFfXEfJ2nFdMt5Go1GT+J9Wvnl2LgddzbLadLG/bWB40B3HMfVCez7CGl7bdEV22tcx9epfqfdl8la79fZX552cj5wHOiu49gr6sLCTa3snw/sf/ax3Dc5Efneoxcr+j7BxM69+nh8cF2Xb5oj0Q6EVxe93vOTrqqCfpqn2E2TC7189UTFje/v+w/0927/+/DHPCs6bdyHpqf0vN59tByJL/M6vWvSnu/I9x6vvJR2yHGgDx2nUhkLP71zqnj08E96Rfz1z73Y86J4pZbaK3dgMIy/PVP8JAInPBk6wJW48zLOzTvWIa5vBm6yEp0HV7bGN44z7ps7ya/rJoc8PL1Pfe44Mp9S3ri95BRP2gna9cI4OA70geMMNM3evjq423pmsknk2caeiZ2qneO44vvl8O6KeUNNnqXExHflTtwPg3YjcZQ/3JEJlHlQW5/9tOLiyzz7vsn1FhcvdfUXHDgwOQ70oeNUm+Zj/X37ZyadVrD9Psxg461ekcvVUfOUupI55zny+cHy2qgufxgy7dZKY/lyGscVHeRW8Vej4TMicdjFm+e/auHgOFDMcSTLl+x+vWFOjZR6c39FHGBm5mQY94MXOkamPwAK6l8x9VSknf+q2/TxrVs9W+mReZSrmTf1b0M4OA7kWxX89xjAcQDhAMIBhAOAcADhAMIBhAMIBwDhAMIBhAMIBxAOAMIBhAMIBxAOIBwAhAMIBxAOIBxAOAAIBxAOIBxAOIBwAJz5X4ABABv0ACu/NIGuAAAAAElFTkSuQmCC'
Hair_02 = 'iVBORw0KGgoAAAANSUhEUgAAAI4AAABMCAYAAAC73Y+3AAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAyZpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDkuMS1jMDAyIDc5LmYzNTRlZmM3MCwgMjAyMy8xMS8wOS0xMjowNTo1MyAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RSZWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZVJlZiMiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIDI1LjQgKFdpbmRvd3MpIiB4bXBNTTpJbnN0YW5jZUlEPSJ4bXAuaWlkOjkyRDJCQkM4QkZCNDExRUU4QUYxOEU1NTFFQjFFQzI3IiB4bXBNTTpEb2N1bWVudElEPSJ4bXAuZGlkOjkyRDJCQkM5QkZCNDExRUU4QUYxOEU1NTFFQjFFQzI3Ij4gPHhtcE1NOkRlcml2ZWRGcm9tIHN0UmVmOmluc3RhbmNlSUQ9InhtcC5paWQ6OTJEMkJCQzZCRkI0MTFFRThBRjE4RTU1MUVCMUVDMjciIHN0UmVmOmRvY3VtZW50SUQ9InhtcC5kaWQ6OTJEMkJCQzdCRkI0MTFFRThBRjE4RTU1MUVCMUVDMjciLz4gPC9yZGY6RGVzY3JpcHRpb24+IDwvcmRmOlJERj4gPC94OnhtcG1ldGE+IDw/eHBhY2tldCBlbmQ9InIiPz7B25SSAAAEiklEQVR42uybzW9MURiH58ogYSq+UmlJJSyw6MJYSNodw0QJtbCTkrBiwQ5/AYKEBEsLsbCsr0prsJPYjEQXYoF0EpU0qUhvEc2YcXvufWXuSU/vx9zpjHiezelt5973nDO/93ffc3JqVavVFEBUFjEFgHAA4QDCAYQDgHAA4QDCAYQDCAcA4QDCAYQDCAcQDgDCAYQDCAcQDvwvpOUHy7JUu3fvgGo7O1erdnz8a6xDyV1d7eqBpdKEuh4ZuRvqvqTiC85zLO85sfrhjCPljaO6EPGTHn97e5uKPzFhzxk/7plzHAdiYYni8vljcyq9v3+n74ZMZnmoB9+79yJSxpkyTeKHjTs9/d13PTj4OpF+HD26K9LESj/Cxq93/Pq47akp1T5/8W5e58FxoDk1jmBymqiZLvc7GVetzTjJLFPGx3Ua3RGlP3o/Zl02juPJ86L2J2z8uOPX513o6OxQ7W7PKB3nCRUfx4GFcZyVK5ep9tu3H7EUbsp8PePkXSsZHjV+vUgck/OZMl7GrY9fd4Sg+dHjB43f5HRBcb6Mf4kUH8eBBV9VVd134jbfB9pWrEgkkF7ly7t2ZuaXuliyZKkvvh437rveFN+Ja3lx9YyPVeNFHb/EF/Tx1zv/Ml+68+jxX768j+NAE2qc6emppnSgUvkdKn7Y2ip49efGSaf9C0pxGj3jk3IaU/x0evG849fvD+tAphpH4nR0rKXGgRbYxzEpPqlaR6dcLjdl4I2OqzuFjtSWq1a5tYhtL07kufI9yT6O7jyHDu5MZF8Hx4HGOE5SSDXvrF6sMPs1STldUIYGcerU6Y2z7e3bt8aSnA9xHNueqau2Ms3PwMBx1e/Lly6ONeL7xHGgsY4T1wH0jBenkR3bnp7+hjpG3AwWp9m/v6802xaLRcvdH8mov1+/fqNrLieK2t+oq1nT/pbUMufOX1D9zufzqt8fPn5U/d68aVO1nrg4DrRmjWPKgD25AyoDrEWrW3Iitm5drzLz0aNCynMa1T55MjTn57PZ7aV6aqBKpRLJYUzzevbsmZJbK7nnbHK53aodHh5OeTVOqnb19Hl8Ul1s2bIex4EWdJygmkbPBMnAvr59pdoMeFZ43JITILXWyEi0+4rFN6o9efJEyTeh6bTK7HK57KspHjx0TwKuWeOeDpictCM5zCevVrly9Zqqrbq7u0terTVvPx1nmvfvd+7cxHGghRxHVgn6TmTQO3Zo6GmkjsgJQSczVabKDmdSSMbrZ3/rJZvN+mqIIHSn0cedy+1Q1+vWuYaVact4jl2QW9R8j46ONlU4OA7E4u95nCNHTqS8TFS/6O3ZppS/YUO774a3ntLHxtxFRKHwPJGOyH6O6f+JojqQOIye2eI0r14NNmRCa1YxqdpVjG3/VO3795998U37WI3qnw7/5QDNcZze3sNNVb7uPIKzCpHaIFJqmFYvCz2eVgfHgeY4DgCOAwgHEA4gHEA4AAgHEA4gHEA4AAgHEA4gHEA4gHAAEA4gHEA4gHAA4QAgHEA4gHAA4QDCAUA4gHAA4cA/yx8BBgDJ2Eb8x2POjwAAAABJRU5ErkJggg=='
Hair_03 = 'iVBORw0KGgoAAAANSUhEUgAAAI4AAABMCAYAAAC73Y+3AAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAyZpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDkuMS1jMDAyIDc5LmYzNTRlZmM3MCwgMjAyMy8xMS8wOS0xMjowNTo1MyAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RSZWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZVJlZiMiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIDI1LjQgKFdpbmRvd3MpIiB4bXBNTTpJbnN0YW5jZUlEPSJ4bXAuaWlkOjk5NzY5N0JBQkZCNDExRUVBMTg5ODMyQTYzNDAwOEZFIiB4bXBNTTpEb2N1bWVudElEPSJ4bXAuZGlkOjk5NzY5N0JCQkZCNDExRUVBMTg5ODMyQTYzNDAwOEZFIj4gPHhtcE1NOkRlcml2ZWRGcm9tIHN0UmVmOmluc3RhbmNlSUQ9InhtcC5paWQ6OTk3Njk3QjhCRkI0MTFFRUExODk4MzJBNjM0MDA4RkUiIHN0UmVmOmRvY3VtZW50SUQ9InhtcC5kaWQ6OTk3Njk3QjlCRkI0MTFFRUExODk4MzJBNjM0MDA4RkUiLz4gPC9yZGY6RGVzY3JpcHRpb24+IDwvcmRmOlJERj4gPC94OnhtcG1ldGE+IDw/eHBhY2tldCBlbmQ9InIiPz6KOuckAAAFQ0lEQVR42uyaTWhUVxTH36Rjk8lIojGRJmkcktSqoA0YlSCVLloUQdEutARqu5JCpYt2UYpd66KFdlEURCgYhUAtVRAXkS6sUilqglMrxmocJjEz0ebDMU6SJnHG57n3tN6X9zlvkvHj/9vcufPm3XPum//9v/M+AtlsVgPAK0U4BADCARAOgHAAhAMAhAMgHADhAAgHQDgAQDgAwgEQDoBwAIQDAIQDIBwA4QAIB7wsBPlDIBCgduPGj6h9Y2Ga2lsjYVcvJS9YVKn0l1WO04A3BkPU/6n9O1cJ7Wz9gvfX5P5K/PtDg54mqM8jIOdB/TNn2uY0D6/xOW5DWYrartiUr5fC68MPKH4sXabE9/uuORwH5ESAlbdp08emTvPZ2riyQ3VtjauBvzlfTW0kPEKKj6cX2jqP1Qr/ckPS04SS/Qml/8OliKeVz3noeWsyb095WMVfWZOh+H8likzj53v+E4NinMOx5abO09FxBI4DCljjMH6dhhW/q0G0R28303gTY2MBu/307XKllea00ox5ch48D33l80ndNI/167dTmxoZFk6jVWTFPDrleO6OA2+PRXuo3b99itq9J+fZxvc7f6PT1Tc1Urtb62bnsY0PxwFz6zjVJULxyYlSX0o3wlcfkYpHylUbn+O5XxUUVxF9Q2OzOmGeJ8d9+PABtUvLRU1wM6XRysxmMmKHBvv5WjlQSWXI8PuIaXymrvxfEX9gzLRWcQvHZcfjvhZT5w/HAYV1HN1paKXtru+W34R8OQ3jVGNMToqV1jdarMRP9oc81VZOefG4fK7X4yp53EyJq5jPVyVkjRBSapsZNYl0gqSWcJWnY/wBMX+uiWLRcdOahZ3E2Gdn4bx4Ox8PY3y/tQ4cB/hzHD7XG1fUzHN1fslkHpnG9+psbuE4wWDQZW1icdWmJVzlaaxRrOL/P/+QbT5Wfccax+J/huOAwt7HsVoxRuU63cdY82l75Onv9auIuNnvp6enCzJxq7hW+V8+2Br34oBOV0NW8dkpnPJxwmu+cBzwbDiOlfNs3fcbrYD9Hzb1PmnXLn+Nvj/1+w1q31tdR+3VfqHNnp4oVfGNjU05xcsVt/dBNr8VpPy+PRFT8mf0edH2t1dUUf9S9wC1e49Fl9D2r9+J53Lfxel+TNvpK4Gn8/m1q892P/7dsY4/ab93V1Zm4Tjg+XMc4wr+oKWuV644uSVqu9/du3F2HjUBeXVhdc7P1wqeMXEZ99y5n6m9cMH+91YrnY+D1zyd5s2O3roh4sppjHlWhSNynGv04fgn6+JwHPDsOM78+WXyk30VvuPQRVLwjuba/Ci36BUZv9RVfL/wPPmOtV8yUxnluDit7JnxheO0LB6lmuRIl3iWxMe3/XxuRsH76eP0ynFp/JbaUTgOKBz/vQG4a8v71N6bKjM8sxL0/CPeoOuM36f+8c7+vCTAT4nrw+KOZixtHt8vVm/CuX0H2Ql2iObIAmobq9R3tTn+4nkivn6c8xrfK3jnGBS2xrmTLpbnXvNnGfoKovarX67lNYE9r4v7FQfuiH5d8TCtyO+v1ihPq3NFH4faFYuGpdNUzMpKZwfeuca89uNnRJOviuN89mzbcy0cOA7w5zhc5XN1/3eqhPpvlk/MagLbfjyk9Pnd36Xl44rz5AqPc30oJO/XzNlKV46jflyp/ePeiyEcOA7wd1UFABwHQDgAwgEQDoBwAIBwAIQDIBwA4QAA4QAIB0A4AMIBEA4AEA6AcACEAyAcAOEAAOEACAdAOADCARAOABAOgHAAhAMgHADhAODIYwEGALi+W+Uy5XndAAAAAElFTkSuQmCC'
Hair_04 = 'iVBORw0KGgoAAAANSUhEUgAAAI4AAABMCAYAAAC73Y+3AAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAyZpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDkuMS1jMDAyIDc5LmYzNTRlZmM3MCwgMjAyMy8xMS8wOS0xMjowNTo1MyAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RSZWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZVJlZiMiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIDI1LjQgKFdpbmRvd3MpIiB4bXBNTTpJbnN0YW5jZUlEPSJ4bXAuaWlkOjlGRkZDQjE5QkZCNDExRUVCNTA2OTZENDI0RTI3OTMwIiB4bXBNTTpEb2N1bWVudElEPSJ4bXAuZGlkOjlGRkZDQjFBQkZCNDExRUVCNTA2OTZENDI0RTI3OTMwIj4gPHhtcE1NOkRlcml2ZWRGcm9tIHN0UmVmOmluc3RhbmNlSUQ9InhtcC5paWQ6OUZGRkNCMTdCRkI0MTFFRUI1MDY5NkQ0MjRFMjc5MzAiIHN0UmVmOmRvY3VtZW50SUQ9InhtcC5kaWQ6OUZGRkNCMThCRkI0MTFFRUI1MDY5NkQ0MjRFMjc5MzAiLz4gPC9yZGY6RGVzY3JpcHRpb24+IDwvcmRmOlJERj4gPC94OnhtcG1ldGE+IDw/eHBhY2tldCBlbmQ9InIiPz5lBoJ0AAAFD0lEQVR42uybwWscVRzHZza7s212s21MU0xbIjVVmkNREAR7K0KKh4IHEUXQo0fBP0Tw6NGCiNJbD9JAofRQUVArQiuNIWxIqe02Ntnsxt3sZtfpe/MzeZOdnZmdzW6qn8/l7dudeb/fe/n+fvObmRe73W5bAHFJsQSAcADhAMIBhAOAcADhAMIBhAMIBwDhAMIBhAMIBxAOAMIBhAMIBxAO/F9IywfbtlU7N/ehanOpumqrrWykTclHJ44Z/UOtshqwliqo/rdffxbJoXff/1TOt7zzDftrq49jTdCdh+3NQ/Xn5y8P1I+49sXuSK2k2tWqnWhTeNb6W9mvW4cN+0n3mpNxoCdsUd7Fix91zDSnsyUzk2SjDfwgM6vaTFNnnka6e+YJivCpxt1YE6rVzf5SfTJW5Isfrt+W53csP4Lsj6W1/Y1mZ/v9nn+lvqXaknWyY+a5du1LMg4MscYRkmYaUfx4XUfKk/ysGq+2uWl3PW9zU38Y7S3S/H6KHzIPN/Llot7Rj/Pn31bt+pO/VHtk/Dl1/HhF+1GLuA7y++OyjvjZgrZ/t9zdftL5+zPdsYKjP5TvS+bpap+MA4PNOBlLS7ZhZRMp3Y/cfeSdtnHXJtd46duNine8jrypwv5MWOYpdisVXVPk0g3VbpTXlKPtVktnzmz3+QZloHzW6Xi8377gtKvG/MWu1CpREbuS8aRfqpv2yTgw3IzjZhoVaZPWfYmBRJlGCKsxtrZkINN+re7Eqq3C/JJx5Vrv2jX8qDYzurbLb3g1Qr3reDuZIJqfYfbL3vylJpKM4a9Z5Ht/XzKL+CW/i/9++0lrHTIOJMs4cq2fzJsRFXSt7het1nZH+3EzW1TETjqdjlWb7K1pnEh++muUIPvyvVXo7k9QP6zG2WOHGgcOxHOcoIjxKzfsOcbnV757Yff37l1EsdPxzWZzKBMPshvk/yfvvFWMkwHD7oaC7PtrmyB/wojrLxkHDkbGCco8X1zVEXDpjdeXn7anjk+o738vPlDtS6ee13cLDR0yi4u/qip+ZuaVnuz1XNNEfA5yYqyp/Pth4ZHhv+DOS/3+4okp1V95tKraq9//OP20/fiSjvC4z13Cnsf8fK9o7/ZnYeXPrufJcbcXltV5Z6en22QcePYyjj+CXz0zs+xFXKTzHj4sSuYxHfDuLoKu+f2K4D0T9+zevHkl0vE7kX7b+F7WIa6fYfOWjP7ay2ciZRq/n4XRvDHOB3NvFsk4cHAyTj4vDxA2up7w1fx1peBzM6f7o9zUiGd/NJL9xLWDN8+dJ9bJ2G63jHUJi+y99nXGOeroJ8l3VvTbeVnfn+790ZNfcp47zrI3rhp/6rhDxoEDkHFS21WlyNLISd87K81qWe/kk0j4bXGpLw44jr7rkh1q8i7Fbz8p/p1wlnO4L+PKOkhkyzpNFMw9ymJf1tlxcqp/48Y3+/oH9v+dfrlDjQND5N89xxcuvCfXXuMt8e5jvWv5vjgi+1NGvL2+6zUryI9YLFXGVHvkkPZ/29v7HPW/HeLi1jjysd3JDzfD2oPINGHwXw4w3BpHqnyp7qtN/VMuPZh3SZIBZO9vLt2wvUhNFBoyznoto/q3bl0e1Noa6+iuq2rXtv4bwiHjQLIaB4CMAwgHEA4gHEA4AAgHEA4gHEA4AAgHEA4gHEA4gHAAEA4gHEA4gHAA4QAgHEA4gHAA4QDCAUA4gHAA4QDCAYQDEMo/AgwAwK83m9hRz20AAAAASUVORK5CYII='


width, height = 400, 200

is_selecting = False
init_sx, init_sy = None, None
sx, sy = None, None

projectName = "/VtubemonCharacterCreation"
data = ['body/Body_32x32_01.png', 'body/Body_32x32_02.png', 'hair/Hair_01.png', 'hair/Hair_02.png', 'hair/Hair_03.png', 'hair/Hair_04.png']
order = ["body","hair"]

indexDict = {}
dictionary = {}

previewImage = None

def initDict(path):
    dictTemp = {}
    i = 0

    for f in os.listdir(path):
        dictTemp[str(i)] = path + "/" + f
        i = i + 1
    return dictTemp

async def draw_image():
    global previewImage

    img_html = js.document.getElementById("preview")

    metadata = set_metadata()
     
    # Get images
    images = await get_images()
    image_name = images[0].name
    images = await convert_to_python_image(images)
    
    js.console.log("1", images[0].width, images[0].height)
    images = resize(images)
    js.console.log("4", images[0].width, images[0].height)

    my_image = images[0]
    for x in range(1,len(images)):
        my_image.paste(images[x], (0,0), mask = images[x])

    # store the final image
    my_stream = BytesIO()
    my_image.save(my_stream, format="PNG", pnginfo=metadata)
    previewImage = my_image

    # convert it in js png file
    image_file = File.new([Uint8Array.new(my_stream.getvalue())], image_name, {type: "image/png"})
    
    # only useful with the first loading
    img_html.classList.remove("loading")
    img_html.classList.add("ready")
    
    # change html image src
    img_html.src = window.URL.createObjectURL(image_file)

async def get_images():
    images = []

    for value in order:
        image = get_image(value)
        images.append(image)

    return images

async def convert_to_python_image(images):
    for x in range(len(images)):
        images[x] = await js_image_to_python_image(images[x])
    
    return images

def set_metadata():
    metadata = PngInfo()
    metadata.add_itxt("Copyright", "Réalisé à partir des tiles de Limezu (https://limezu.itch.io/)")
    metadata.add_itxt("Seed", get_seed())
    return metadata

# Get image from pyodide to an png file used by js
def get_image(shape):
    image_file = get_image_from_pyodide(dictionary[str(shape)][str(indexDict[str(shape)])], str(shape) + ".png")
    return image_file

def get_image_from_pyodide(path, name):
    f = open(path, 'rb')
    image_file = File.new([Uint8Array.new(f.read())], name, {"type": "image/png"})
    return image_file

# Transform a png file (js) to an Image from Pil
async def js_image_to_python_image(jsImage):
    array_buf = Uint8Array.new(await jsImage.arrayBuffer())
    bytes_list = bytearray(array_buf)
    my_bytes = BytesIO(bytes_list) 
    return Image.open(my_bytes)

def resize(images):
    js.console.log("2", images[0].width, images[0].height)
    for index in range(len(images)) :
        images[index] = images[index].resize((130, 72),Image.NEAREST, (0,0,130,72))
    js.console.log("3", images[0].width, images[0].height)
    return images

def get_seed():
    seed = ""
    for value in order :
        seed += '{}-{};'.format(str(value), dictionary[str(value)][str(indexDict[str(value)])].replace("/assets/"+value+"/","").replace(".png",""))

    return seed

def change_seed_in_seed_area():
    seed = get_seed()
    textElement = js.document.getElementById("seedArea") 
    textElement.innerText = seed

# Buttons
async def plus(event):
    shape = list(set(event.target.className.split(' ')) & set(order))[0]
    indexDict.update({str(shape): await index_change_operation(dictionary[str(shape)], indexDict[str(shape)], 1)})
    await after_index_change(str(shape))

async def minus(event):
    shape = list(set(event.target.className.split(' ')) & set(order))[0]
    indexDict.update({str(shape): await index_change_operation(dictionary[str(shape)], indexDict[str(shape)], -1)})
    await after_index_change(str(shape))

async def index_change_operation(dictionary, index, operation):
    index += operation
    if operation < 0 and index < 0 :
        index = len(dictionary) - 1

    elif operation > 0 and index >= len(dictionary) :
        index = 0
    
    return index

async def after_index_change(nameIndex):
    displayIndex(nameIndex)
    await draw_image()
    change_seed_in_seed_area()

def copy_seed(ev):
    seed = get_seed()

    navigator.clipboard.writeText(seed)

def dl_preview(ev):
    global previewImage

    metadata = set_metadata()
    previewImage = previewImage.resize((200,100), Image.NEAREST)

    my_stream = BytesIO()
    previewImage.save(my_stream, format="PNG", pnginfo=metadata)
    image_file = File.new([Uint8Array.new(my_stream.getvalue())], "unused_file_name.png", {type: "image/png"})
    url = js.URL.createObjectURL(image_file)

    hidden_a = js.document.createElement('a')
    hidden_a.setAttribute('href', url)
    hidden_a.setAttribute('download', "new_image.png")
    hidden_a.click()

async def randomize(ev):
    for value in order:
        indexDict.update({str(value): random.randrange(len(dictionary[str(value)]))})
        await after_index_change(value)

# display index
def displayIndex(shape):
    textIndexes = js.document.querySelectorAll(".index."+shape) 
    for element in textIndexes:
        element.innerText = dictionary[str(shape)][str(indexDict[str(shape)])].replace("/assets/"+str(shape)+"/","").replace(".png","")

async def init_assets():
    global data
    path = "/assets"
    os.mkdir(path) 

    for info in data:
        path = "/assets/" + info.split('/')[0]

        if not os.path.exists(path):
            os.mkdir(path) 

        url = "https://tortuedebois.github.io" + projectName + "/assets/" + info
        response = await pyfetch(url)

        with open("/assets/" + info, mode="wb") as f:
            f.write(await response.bytes())


    # files = os.listdir('/assets')
    # for file in files:
    #     js.console.log(file)

    #     for f in os.listdir('/assets/' + file):
    #         js.console.log("\t" + f)

def init_data():
    """
    Récupérer toutes les imgs. Selon la nomenclature:
    $path/<folder>/<file>
    """
    # data = []
    # for f in os.listdir(str(Path.cwd()) + "/assets/"):
    #     for file in os.listdir(str(Path.cwd()) + "/assets/" + f + "/"):
    #         data.append(f + "/" + file) #Trouver une alternativeà "append" car risque d'explosion en compléxité (temps ET mémoire)
    # print(data)

    global dictionary, indexDict

    files = os.listdir('/assets')
    for file in files:
        if file not in dictionary :
            dictionary[str(file)] = initDict("/assets/" + file)
            indexDict[str(file)] = 0

async def main():
    await init_assets()
    init_data()
    for value in order :
        displayIndex(value)
    await draw_image()
    change_seed_in_seed_area()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
