using Python.Runtime;

Runtime.PythonDLL = "python311.dll";

PythonEngine.Initialize();

dynamic tf = Py.Import("tensorflow");
dynamic np = Py.Import("numpy");

dynamic model = tf.keras.models.load_model("model.keras");

dynamic list = new PyList();
list.append(tf.keras.utils.load_img("tests/kkk.jpg"));
dynamic data = np.array(list);
dynamic result = model.predict(data);

Console.WriteLine("Previsões:");
Console.WriteLine(result);

PythonEngine.Shutdown();
