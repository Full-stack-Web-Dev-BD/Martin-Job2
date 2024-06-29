// See https://aka.ms/new-console-template for more information
using log4net.Config;
using log4net;
using Microsoft.Extensions.DependencyInjection;
using RocketSource;
using System.Reflection;

IServiceCollection services = new ServiceCollection();
Startup startup = new Startup();
startup.ConfigureServices(services);
IServiceProvider serviceProvider = services.BuildServiceProvider();
var logRepository = LogManager.GetRepository(Assembly.GetEntryAssembly());
XmlConfigurator.Configure(logRepository, new FileInfo("log4net.config"));
IRocketSourceService svc = serviceProvider.GetService<IRocketSourceService>();
svc.ProcessScans();
