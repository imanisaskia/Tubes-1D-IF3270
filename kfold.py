import id3
import mlp
import pandas

def ID3(k, df, pruning, is_result_continuous):
    
    num_data_per_fold = round(len(df.index) / k)
    trees = []
    trees_accuracy = []
    
    # Creating models and counting accuracy
    for i in range(k):
        first_idx_val = i * num_data_per_fold
        last_idx_val = (i+1) * num_data_per_fold - 1

        if (first_idx_val != 0 and last_idx_val != (len(df.index) - 1)):
            df_training_top = df.iloc[:first_idx_val, :].reset_index(drop = True)
            df_training_bottom = df.iloc[(last_idx_val + 1):, :].reset_index(drop = True)
            df_training = pandas.concat([df_training_top, df_training_bottom])
        elif (first_idx_val == 0 and last_idx_val != (len(df.index) - 1)):
            df_training = df.iloc[(last_idx_val + 1):, :].reset_index(drop = True)
        elif (first_idx_val != 0 and last_idx_val == (len(df.index) - 1)):
            df_training = df.iloc[:first_idx_val, :].reset_index(drop = True)
        else:
            df_training = pandas.DataFrame()

        df_validation = df.iloc[first_idx_val:last_idx_val, :].reset_index(drop = True)

        print("-------------------- MODEL", i+1, "--------------------")

        # We use the whole training data for pruning validation
        result_tree = id3.ID3(df, df_training, df_validation, pruning)
        trees.append(result_tree)

        result_accuracy = id3.count_accuracy(result_tree, [], df_validation, is_result_continuous)
        trees_accuracy.append(result_accuracy)
    
        # Printing each model and its accuracy
        
        id3.print_tree(trees[i], 0)
        print("ACCURACY:", trees_accuracy[i])
        print("")

    best_tree_idx = 0
    best_accuracy = trees_accuracy[0]
    for i in range(k):
        if (trees_accuracy[i] > best_accuracy):
            best_tree_idx = i
            best_accuracy = trees_accuracy[i]

    return trees[best_tree_idx]

def MLP(k, df, num_perceptrons_in_layer, max_iteration, error_threshold, learning_rate, batch_size):
    
    num_data_per_fold = round(len(df.index) / k)
    models = []
    models_accuracy = []
    
    # Creating models and counting accuracy
    for i in range(k):
        first_idx_val = i * num_data_per_fold
        last_idx_val = (i+1) * num_data_per_fold - 1

        if (first_idx_val != 0 and last_idx_val != (len(df.index) - 1)):
            df_training_top = df.iloc[:first_idx_val, :].reset_index(drop = True)
            df_training_bottom = df.iloc[(last_idx_val + 1):, :].reset_index(drop = True)
            df_training = pandas.concat([df_training_top, df_training_bottom])
        elif (first_idx_val == 0 and last_idx_val != (len(df.index) - 1)):
            df_training = df.iloc[(last_idx_val + 1):, :].reset_index(drop = True)
        elif (first_idx_val != 0 and last_idx_val == (len(df.index) - 1)):
            df_training = df.iloc[:first_idx_val, :].reset_index(drop = True)
        else:
            df_training = pandas.DataFrame()

        df_validation = df.iloc[first_idx_val:last_idx_val, :].reset_index(drop = True)

        print("-------------------- MODEL", i+1, "--------------------")

        result_model = mlp.MLP(df_training, num_perceptrons_in_layer, max_iteration, error_threshold, learning_rate, batch_size)
        models.append(result_model)

        result_accuracy = mlp.count_accuracy(result_model, df_validation)
        models_accuracy.append(result_accuracy)
    
        # Printing each model and its accuracy
        
        models[i].print_model()
        print("ACCURACY:", models_accuracy[i])
        print("")

    best_model_idx = 0
    best_accuracy = models_accuracy[0]
    for i in range(k):
        if (models_accuracy[i] > best_accuracy):
            best_model_idx = i
            best_accuracy = models_accuracy[i]

    return models[best_model_idx]
