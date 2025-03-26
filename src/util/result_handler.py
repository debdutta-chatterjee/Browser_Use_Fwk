class ResultHandler:

    @staticmethod
    def save_result(history,file_path,result_class,console=False):
        history.save_to_file(file_path)
        test_result = history.final_result()
        result = result_class.model_validate_json(test_result)
        
        if console:
            print(test_result)
        return result