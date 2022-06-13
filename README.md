# MapReduce con Hadoop en Linux
Intalación de Hadoop en Linux y su implementación de MapReduce. También un ejemplo de su uso con WordCount para contar las repeticiones en un archivo.txt

## Prerrequisitos
#### ***1-Java***
```
sudo apt update

sudo apt install openjdk-8-jdk -y
```

**Para verificar su instalación:**
`java -version`

#### ***2-NanoEditor***
```
sudo apt update

sudo apt-get install nano
```
**Para verificar su instalación:**
`nano`

#### ***3-OpenSSH***
```
sudo apt update

sudo apt install openssh-server openssh-client -y
```
**Para verificar su instalación:**
`ssh -V`

## Instalación y configuración de HADOOP:
#### ***Crearemos un nuevo usuario, en este caso llamado "hdoop" y le daremos permisos de admin. Entonces nos logueamos con el usuario creado***
```
sudo adduser hdoop
sudo adduser hdoop sudo
su - hdoop
```
#### ***Creamos una key que usaremos para la conexión, ponemos esta key en la lista de keys autorizadas y cambiamos los permisos de la misma***
```
ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
chmod 0600 ~/.ssh/authorized_keys
```
**Probamos la conexión del usuario a nuestra localhost:**
`ssh localhost`
#### ***Descargamos Hadoop, en este caso la versión 3.3.2 de la librería de Apache _(los comandos mostrados pueden cambiar con las versiones)_***
```
wget https://downloads.apache.org/hadoop/common/hadoop-3.3.2/hadoop-3.3.2.tar.gz
```
#### ***Descomprimimos el archivo***
```
tar xzf hadoop - 3.3.2.tar.gz
```
## Ahora procederemos a realizar cambios importantes para su correcto funcionamiento.

#### ***Modificaremos el PATH de JAVA para HADOOP, para ello abrirmos el archivo bashrc***
```
sudo nano .bashrc
```
#### ***Pegaremos lo siguiente al final del documento, si aparece ya, borrarlo y pegar este, salimos y guardamos con Ctrl+X, S***
```
export HADOOP_HOME=/home/hdoop/hadoop-3.3.2
export HADOOP_INSTALL=$HADOOP_HOME
export HADOOP_MAPRED_HOME=$HADOOP_HOME
export HADOOP_COMMON_HOME=$HADOOP_HOME
export HADOOP_HDFS_HOME=$HADOOP_HOME
export YARN_HOME=$HADOOP_HOME
export HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_HOME/lib/native
export PATH=$PATH:$HADOOP_HOME/sbin:$HADOOP_HOME/bin
export HADOOP_OPTS="-Djava.library.path=$HADOOP_HOME/lib/nativ"
```
#### ***Recargamos los cambios***
```
source ~/.bashrc
```
#### ***Abrimos el archivo para indicar la dirección de Java***
```
sudo nano $HADOOP_HOME/etc/hadoop/hadoop-env.sh
```
#### ***Pegamos este texto al final del archivo, salimos y guardamos con Ctrl+X, S***
```
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
```
#### ***Abrimos el archivo***
```
sudo nano $HADOOP_HOME/etc/hadoop/core-site.xml
```
#### ***Pegamos este texto entre _configuration_ _configuration_, salimos y guardamos con Ctrl+X, S***
```
   <property>
        <name>hadoop.tmp.dir</name>
        <value>/home/hdoop/tmpdata</value>
        <description>A base for other temporary directories.</description>
    </property>
    <property>
        <name>fs.default.name</name>
        <value>hdfs://localhost:9000</value>
        <description>The name of the default file system></description>
    </property>
```
#### ***Abrimos el archivo***
```
sudo nano $HADOOP_HOME/etc/hadoop/hdfs-site.xml
```
#### ***Pegamos este texto entre _configuration_ _configuration_, salimos y guardamos con Ctrl+X, S***
```
<property>
  <name>dfs.data.dir</name>
  <value>/home/hdoop/dfsdata/namenode</value>
</property>
<property>
  <name>dfs.data.dir</name>
  <value>/home/hdoop/dfsdata/datanode</value>
</property>
<property>
  <name>dfs.replication</name>
  <value>1</value>
</property>
```
#### ***Aquí editaremos nuestro archivo MapReduce, Abrimos el archivo***
```
sudo nano $HADOOP_HOME/etc/hadoop/mapred-site.xml
```
#### ***Pegamos este texto entre _configuration_ _configuration_ para indicar que nuestro framework es YARN, salimos y guardamos con Ctrl+X, S***
```
<property>
  <name>mapreduce.framework.name</name>
  <value>yarn</value>
</property>
```
#### ***Abrimos el archivo***
```
sudo nano $HADOOP_HOME/etc/hadoop/yarn-site.xml
```
#### ***Pegamos este texto entre _configuration_ _configuration_, salimos y guardamos con Ctrl+X, S***
```
<property>
  <name>yarn.nodemanager.aux-services</name>
  <value>mapreduce_shuffle</value>
</property>
<property>
  <name>yarn.nodemanager.aux-services.mapreduce.shuffle.class</name>
  <value>org.apache.hadoop.mapred.ShuffleHandler</value>
</property>
<property>
  <name>yarn.resourcemanager.hostname</name>
  <value>127.0.0.1</value>
</property>
<property>
  <name>yarn.acl.enable</name>
  <value>0</value>
</property>
<property>
  <name>yarn.nodemanager.env-whitelist</name>
  <value>JAVA_HOME,HADOOP_COMMON_HOME,HADOOP_HDFS_HOME,HADOOP_CONF_DIR,CLASSPATH_PERPEND_DISTCACHE,HADOOP_YARN_HOME,HADOOP_MAPRED_HOME</value>
</property>
```
## Arrancar HADOOP

#### ***Formateamos el namenode de HADOOP***
```
hdfs namenode -format
```
#### ***Nos dirigimos a la ruta de HADOOP***
```
cd ~/hadoop-3.3.2/sbin
```
#### ***Iniciamos HADOOP***
```
./start-dfs.sh
```
#### ***Iniciamos YARN***
```
./start-yarn.sh
```
## Utilizar MapReduce

#### ***Preparación de los archivos descargados:***
#### ***Dentro del Home de nuestro usuario hdoop crearemos una nueva carpeta, en este caso con el nombre "ContadorPalabras"***
#### ***Pondremos el archivo jar y el archivo txt dentro de la carpeta***

#### ***Exportaremos la dirección el PATH de HADOOP***
```
export HADOOP_CLASSPATH=$CLASSPATH=$(hadoop classpath)
```
**Para verificar podemos usar:**
`echo $HADOOP_CLASSPATH`

#### ***Crearemos un directorio en HADOOP llamado "ContadorPalabras"***
```
hdfs dfs -mkdir /ContadorPalabras
```
**Para verificar podemos usar:**
`hdfs dfs -ls /`
#### ***Ahora crearemos una carpeta dentro del ContadorPalabras donde pondremos nuestro archivo de entrada, en este caso la llamaremos "Entrada"***
```
hdfs dfs -mkdir /ContadorPalabras/Entrada
```
#### ***Pondremos nuestro archivo de texto dentro del directorio Entrada***
```
hdfs dfs -put /home/hdoop/ContadorPalabras/frutas.txt /ContadorPalabras/Entrada
```
**Para verificar podemos usar:**
`hdfs dfs -ls /ContadorPalabras/Entrada`

#### ***Ahora ejecutaremos MapReduce con el archivo frutas.txt que está almacenado en HADOOP. Usaremos en este caso la clase wordcount y pondremos los resultados***
#### ***en un nuevo directorio dentro de /ContadorPalabras llamado "Salida"***
```
hadoop jar /home/hdoop/ContadorPalabras/hadoop-mapreduce-examples-3.3.2.jar wordcount /ContadorPalabras/Entrada /ContadorPalabras/Salida
```
#### ***Verificaremos los resultados***
```
hdfs dfs -cat /ContadorPalabras/Salida/*
```


