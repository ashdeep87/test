from factory import get_data_extractor

extractor = get_data_extractor()
data = extractor.get_individual()
print(data)