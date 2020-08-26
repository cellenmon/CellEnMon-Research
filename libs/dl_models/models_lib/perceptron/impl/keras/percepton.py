import config as config
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
from libs.dl_models.dl_model import DLModel


class Perceptron(DLModel):
    def __init__(self, time_scale, prediction_type):

        number_of_links = len(config.signal_names) if config.TEST else len(config.link_names)

        # model
        self.model = Sequential(name="Perceptron_stock_prediction_of_" + time_scale)

        super().__init__(self.model, config.DL_config, time_scale)

        # input layer
        if time_scale == '15m': # <number of stocks> x <training size>
            self.model.add(Flatten(input_shape=(number_of_links, int(int(
                config.max_window_size[time_scale] * 0.5) * 0.7)),
                                   name=f'time_scale_{time_scale}'))
        else:  # low,open,close,high,volume | <numebr of stocks> x 4 x <training size>
            self.model.add(
                Flatten(input_shape=(int(int(config.max_window_size[time_scale] * 0.5) * 0.7), number_of_links, 4),
                        name=f'time_scale_{time_scale}'))

        # output layer

        # MANY2ONE
        if prediction_type == config.MANY2ONE:
            if time_scale == '15m': # 1 x <prediction size>
                self.model.add(Dense(int(int(config.max_window_size[time_scale] * 0.5) * 0.3),
                                     name=f'time_scale_{time_scale}_output'))
            else:  # low,open,close,high,volume | 4 x <prediction size>
                self.model.add(Dense(4 * int(int(config.max_window_size[time_scale] * 0.5) * 0.3),
                                     name=f'time_scale_{time_scale}_output'))


        # MANY2MANY
        else:
            if time_scale == '15m':  # <number of stocks> x <prediction size>
                self.model.add(Dense(number_of_links * int(int(config.max_window_size[time_scale] * 0.5) * 0.3),
                                     name=f'time_scale_{time_scale}_output'))

            else:  # low,open,close,high,volume | <number of stocks> x 4 x <prediction size>
                self.model.add(Dense(number_of_links * 4 * int(int(config.max_window_size[time_scale] * 0.5) * 0.3),
                                     name=f'time_scale_{time_scale}_output'))

        self.model.compile(loss='mse', optimizer='adam')
