from math import floor, ceil, sqrt
from roman import toRoman

VOLTAGE_TIERS = ["ULV", "LV", "MV", "HV", "EV", "IV", "LuV", "ZPM", "UV", "UHV", "UEV"]

print("Mining Drone,Drone Tier,Output,Output Type,Chance,Min Size,Max Size,Min Distance,Max Distance,Min Computation,"
      "Min Module,Duration,EU/t,Weight")

with open("input.txt", "r") as input_file:
    for line in input_file:
        raw_chances, raw_outputs, remainder = line.strip().split("}, ")
        material_type, min_size, max_size, min_distance, max_distance, computation_required, min_module_required, \
            raw_duration, raw_eut, raw_start_drone_tier, raw_end_drone_tier, weight = remainder.split(", ")

        chances = raw_chances[2:-1].split(", ")
        outputs = raw_outputs[2:-1].split(", ")

        assert len(chances) == len(outputs)

        duration = eval(raw_duration)
        _, _voltage_tier = raw_eut.split("[")
        voltage_tier, _ = _voltage_tier.split("]")
        eut = floor(30 * int(voltage_tier) / 32)

        start_drone_tier = VOLTAGE_TIERS.index(raw_start_drone_tier)
        end_drone_tier = VOLTAGE_TIERS.index(raw_end_drone_tier)

        for _, (chance, output) in enumerate(zip(chances, outputs)):
            chance_float = int(chance) / 10000
            drone_tier_range = range(start_drone_tier, end_drone_tier + 1)
            for drone_tier in drone_tier_range:
                print(",".join([str(i) for i in [
                    f"Mining Drone MK-{toRoman(drone_tier)}",
                    VOLTAGE_TIERS[drone_tier],
                    output,
                    material_type,
                    chance_float,
                    int(min_size) + 2 ** (drone_tier - start_drone_tier) - 1,
                    int(max_size) + 2 ** (drone_tier - start_drone_tier) - 1,
                    min_distance,
                    max_distance,
                    computation_required,
                    min_module_required,
                    ceil(duration / sqrt(drone_tier - start_drone_tier + 1)),
                    eut,
                    weight,
                ]]))
