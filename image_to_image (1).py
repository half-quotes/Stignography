from PIL import Image

MAX_COLOR_VALUE = 256
MAX_BIT_VALUE = 8

def make_image(data, resolution):
    image = Image.new("RGB", resolution)
    image.putdata(data)
    return image

def remove_n_least_significant_bits(value, n):
    value = value >> n 
    return value << n

def get_n_least_significant_bits(value, n):
    value = value << MAX_BIT_VALUE - n
    value = value % MAX_COLOR_VALUE
    return value >> MAX_BIT_VALUE - n

def get_n_most_significant_bits(value, n):
    return value >> MAX_BIT_VALUE - n

def shit_n_bits_to_8(value, n):
    return value << MAX_BIT_VALUE - n

def encode(image_to_hide, image_to_hide_in, n_bits):

    width, height = image_to_hide.size

    hide_image = image_to_hide.load()
    hide_in_image = image_to_hide_in.load()

    data = []

    for y in range(height):
        for x in range(width):

            r_hide, g_hide, b_hide = hide_image[x,y]
            r_hide = get_n_most_significant_bits(r_hide, n_bits)
            g_hide = get_n_most_significant_bits(g_hide, n_bits)
            b_hide = get_n_most_significant_bits(b_hide, n_bits)

            # remove lest n sig bits
            r_hide_in, g_hide_in, b_hide_in = hide_in_image[x,y]

            r_hide_in = remove_n_least_significant_bits(r_hide_in, n_bits)
            g_hide_in = remove_n_least_significant_bits(g_hide_in, n_bits)
            b_hide_in = remove_n_least_significant_bits(b_hide_in, n_bits)

            data.append((r_hide + r_hide_in, 
                         g_hide + g_hide_in,
                         b_hide + b_hide_in))

    return make_image(data, image_to_hide.size)

def decode(image_to_decode, n_bits):
    width, height = image_to_decode.size
    encoded_image = image_to_decode.load()

    data = []

    for y in range(height):
        for x in range(width):

            r_encoded, g_encoded, b_encoded = encoded_image[x,y]
            
            r_encoded = get_n_least_significant_bits(r_encoded, n_bits)
            g_encoded = get_n_least_significant_bits(g_encoded, n_bits)
            b_encoded = get_n_least_significant_bits(b_encoded, n_bits)

            r_encoded = shit_n_bits_to_8(r_encoded, n_bits)
            g_encoded = shit_n_bits_to_8(g_encoded, n_bits)
            b_encoded = shit_n_bits_to_8(b_encoded, n_bits)

            data.append((r_encoded, g_encoded, b_encoded))

    return make_image(data, image_to_decode.size)

if "_main_":
    image_to_hide_path = "./c.jpeg"
    image_to_hide_in_path = "./d.jpeg"
    encoded_image_path = "./encoded.jpeg"
    decoded_image_path = "./decoded.jpeg"
    n_bits = 6

    image_to_hide = Image.open(image_to_hide_path)
    image_to_hide_in = Image.open(image_to_hide_in_path)
    print(image_to_hide.size)
    print(image_to_hide_in.size)
    # image_to_hide.resize((259,194))
    # image_to_hide_in = image_to_hide_in.resize((259,194), Image.ANTIALIAS)
    # print(image_to_hide.size)
    # print(image_to_hide_in.size)
    # # image_to_hide_in.resize((40,40))
    encode(image_to_hide, image_to_hide_in, n_bits).save(encoded_image_path)

    image_to_decode = Image.open(encoded_image_path)
    decode(image_to_decode, n_bits).save(decoded_image_path)