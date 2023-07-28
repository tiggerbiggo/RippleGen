import os
import random
import math
import numpy as np
from PIL import Image
from FileUtil import generate_filename

#This is the script that does the image generation.
#Below are ranges for the parameters;

line_count = 200 # number of generated sine waves in each image
angle_range = (0, 360)
phase_offset_range = (0, 360)
magnitude_range = (1, 100)
frequency_range = (1, 300)
red_range = (0, 255)
green_range = (0, 255)
blue_range = (0, 255)

#Below are the settings for standing waves
#Standing waves are 2 identical waves at 180 degrees rotation
#All parameters are relative to the "pure" standing wave, e.g
#angle range is the random range of angle difference for the
#opposing wave relative to its standard 180 degrees

#Using standing waves will increase the render time as it will
#be processing more waves
sw_probability = 0
sw_angle_range = (0, 0)
sw_phase_range = (0, 0)
sw_magnitude_range = (0, 0)

#Harmonic series
harmonic_probability = 0
harmonic_base_freq_range = (1, 5)
harmonic_count_range = (5, 10)
harmonic_decay = 0.6

output_dir = '.'

def make_random_lines(num_lines):
    lines = []
    for i in range(num_lines):
        percent = i / num_lines
        magnitude = random.uniform(*magnitude_range)
        do_harmonic = random.random() < harmonic_probability
        frequency = 0
        if do_harmonic:
            frequency = random.uniform(*harmonic_base_freq_range)
        else:
            frequency = random.uniform(*frequency_range)
        params = [
            random.uniform(*angle_range),
            random.uniform(*phase_offset_range),
            magnitude * (1 / frequency) * percent,
            frequency,
            random.uniform(*red_range),
            random.uniform(*green_range),
            random.uniform(*blue_range),
        ]
        lines.append(' '.join(map(str, params)))
        if random.random() < sw_probability:
            params = [
                params[0] + random.uniform(*sw_angle_range) + 180,
                params[1] + random.uniform(*sw_phase_range),
                params[2] + random.uniform(*sw_magnitude_range),
                params[3],
                params[4],
                params[5],
                params[6]
                ]
            lines.append(' '.join(map(str, params)))
        if do_harmonic:
            harmonic_count = random.randint(*harmonic_count_range)
            for h in range(harmonic_count):
                params = [
                    params[0],
                    params[1],
                    params[2] * harmonic_decay,
                    params[3] * 2,
                    params[4],
                    params[5],
                    params[6]
                    ]
                lines.append(' '.join(map(str, params)))
    return lines

def parse_data(lines):
    data = []
    for line in lines:
        numbers = list(map(float, line.split()))
        data.append(numbers)
    return data

def animate_phase(params, image_count, image_size):
    images = []
    phaseInit = []
    for idx, param_set in enumerate(params):
        phaseInit.append(param_set[1])
    for i in range(image_count):
        print(i)
        percent = i/image_count
        percent *= 360
        for j in range(len(params)):
            phaseShift = percent
            phaseShift *= math.ceil((params[j][3] / 1000) * 100)
            params[j][1] = phaseInit[j] + phaseShift
        images.append(make_image(image_size, params))
    images[0].save(generate_filename("output_anim", "gif"), save_all=True, append_images=images[1:], optimize=False, duration=0, loop=0)

def make_image(image_size, params):
    # Initialize 2D arrays for each color channel
    red_channel = np.zeros(image_size, dtype=np.float32)
    green_channel = np.zeros(image_size, dtype=np.float32)
    blue_channel = np.zeros(image_size, dtype=np.float32)

    param_count = len(params)
    # Iterate over the number of lines for this image
    for idx, param_set in enumerate(params):
        # Apply the parameters to the color channels
        angle, phase_offset, magnitude, frequency, red, green, blue = param_set

        #define an attenuation function to make subsequent waves less impactful
        #seems to improve variation but you can disable it by setting attenuate to 1
        #attenuate = idx / param_count # percentage 0 - 1 for which param we are
        #attenuate += 2 # shift the log graph over
        #attenuate = math.log(attenuate)
        #attenuate = 1 # uncomment to disable attenuation
        
        frequency = frequency / 100
        angle_rad = np.radians(angle)
        phase_offset_rad = np.radians(phase_offset)
        y, x = np.ogrid[:image_size[0], :image_size[1]]
        coords = x * np.cos(angle_rad) + y * np.sin(angle_rad)
        #sine_wave = (magnitude * attenuate * (2/frequency)) * np.sin(frequency * coords + phase_offset_rad)
        sine_wave = magnitude * np.sin(frequency * coords + phase_offset_rad)
        red_channel += red * sine_wave
        green_channel += green * sine_wave
        blue_channel += blue * sine_wave
    # Normalize the color channels
    #max_value = max(red_channel.max(), green_channel.max(), blue_channel.max())
    red_channel = (red_channel / red_channel.max()) * 255
    green_channel = (green_channel / green_channel.max()) * 255
    blue_channel = (blue_channel / blue_channel.max()) * 255

    red_channel = np.abs(red_channel)
    green_channel = np.abs(green_channel)
    blue_channel = np.abs(blue_channel)
    
    # Convert to integers
    red_channel = np.clip(red_channel, 0, 255).astype(np.uint8)
    green_channel = np.clip(green_channel, 0, 255).astype(np.uint8)
    blue_channel = np.clip(blue_channel, 0, 255).astype(np.uint8)

    # Combine the color channels to create the final image
    return Image.merge("RGB", [Image.fromarray(channel) for channel in [red_channel, green_channel, blue_channel]])

def make_random_image(image_size):
    lines = make_random_lines(line_count)
    params = parse_data(lines)
    return make_image(image_size, params), params
