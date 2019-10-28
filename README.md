# dscrecover
Instructions and script for recovering the installer code of DSC alarm systems. At the time of upload, this has only been tested on DSC PC1832 but it is assumed to work on PC1616, PC1864, and potentially others. 

Required components:
* [DSC IT-100 integration module](https://www.dsc.com/alarm-security-products/IT-100%20-%20PowerSeries%20Integration%20Module/22) (these can sometimes be found on ebay for less than $30 USD plus shipping)
* USB 2.0 to RS232 DB9 Serial Cable. I have found [this one](https://www.amazon.com/gp/product/B00QUZY4L0/ref=ppx_yo_dt_b_asin_title_o02_s00?ie=UTF8&psc=1) works well
* Pretty much any computer with USB 2.0 A port and able to run python. A [Raspberry Pi](https://www.raspberrypi.org/products/)  works well. There is no setup script, just make sure you have python3 and [pyserial](https://pypi.org/project/pyserial/) installed. Windows or macOS should work, but the USB device name will likely be different (see below).
* Some [Hook up wire](https://www.adafruit.com/?q=hook%20up%20wire). Four different colors is nice to have

Once you have all that, connect the IT-100 per instructions. Connect the USB 2.0 to RS232 cable from the IT-100 to your computer that has python3 and pyserial installed. Confirm that the USB serial device shows up as /dev/ttyUSB0. If not you need to find the device and edit the [SERIALDEVICE](https://github.com/bschick/dscrecover/blob/11dec745effe4d227e5daaa26015a250b989a084/findcode.py#L6) variable in the scipt. Once you have the USB serial device name set, you can run the script as root and wait. It takes less than 5 seconds per guess, so worst case is ~half a day for installer codes near the top of the 0-9999 range. Note that the DSC systems this has been tested with do not have lockout for incorrect guesses. Make sure your model does not have a lockout. 


THE SOFTWARE AND INSTRUCTIONS ARE PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
